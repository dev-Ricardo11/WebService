from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse
import xml.etree.ElementTree as ET
from datetime import datetime
from database import DatabaseManager
from xml_processor import XMLProcessor
import os

app = FastAPI(title="Credit Limit Validation Service")

db_manager = DatabaseManager()
xml_processor = XMLProcessor()

@app.get("/")
async def root():
    return {"message": "Credit Limit Validation Service", "status": "running"}

@app.post("/validateCreditLimit", response_class=PlainTextResponse)
async def validate_credit_limit(request: Request):
    try:
        body = await request.body()
        xml_content = body.decode('utf-8')

        request_data = xml_processor.parse_credit_limit_rq(xml_content)

        credit_limit_id = db_manager.save_credit_limit_request(request_data)

        validation_result = validate_credit_limit_logic(request_data)

        db_manager.update_credit_limit_status(
            credit_limit_id,
            validation_result['status'],
            validation_result['message']
        )

        response_xml = xml_processor.generate_credit_limit_rs(
            request_data['CodeClientBackOffice'],
            request_data['CodeClientOBT'],
            validation_result['status'],
            validation_result['message']
        )

        return Response(content=response_xml, media_type="application/xml")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

def validate_credit_limit_logic(request_data: dict) -> dict:
    code_client = request_data.get('CodeClientBackOffice')
    value = request_data.get('value', 0)
    payment_type = request_data.get('paymentType', '')

    previous_requests = db_manager.get_client_requests(code_client)

    total_pending = sum(
        req['value'] for req in previous_requests
        if req['status'] == 'PENDING'
    )

    CREDIT_LIMIT = 1000000.0

    if total_pending + value > CREDIT_LIMIT:
        return {
            'status': 'NO-OK',
            'message': f'El limite de credito ha sido excedido. Limite disponible: {CREDIT_LIMIT - total_pending}. Por favor comunicarse con el departamento de credito.'
        }

    if payment_type == 'TC' and value > 500000:
        return {
            'status': 'NO-OK',
            'message': 'Las transacciones con tarjeta de credito no pueden exceder 500,000. Por favor usar otro medio de pago.'
        }

    return {
        'status': 'OK',
        'message': 'Transaccion aprobada'
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

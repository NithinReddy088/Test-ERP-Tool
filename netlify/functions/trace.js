exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const path = event.path.split('/');
  const traceType = path[path.length - 2]; // 'serial' or 'batch'
  const traceId = path[path.length - 1];

  if (traceType === 'serial') {
    const serialData = {
      serial_no: traceId,
      item_code: "MED-DEV-001",
      status: "In Stock",
      warehouse: "Finished Goods - HC",
      production_history: [
        {
          work_order: "WO-2024-001",
          date: "2024-10-25",
          operation: "Assembly",
          workstation: "Assembly Line 1"
        },
        {
          work_order: "WO-2024-001", 
          date: "2024-10-26",
          operation: "Testing",
          workstation: "QC Station 1"
        }
      ],
      quality_inspections: [
        {
          inspection: "QI-2024-001",
          status: "Accepted",
          date: "2024-10-30",
          inspector: "Sarah Johnson"
        }
      ],
      supplier_info: {
        supplier: "MedTech Components Ltd",
        supplier_batch: "SUPP-BATCH-001",
        received_date: "2024-10-20"
      }
    };

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(serialData)
    };
  }

  if (traceType === 'batch') {
    const batchData = {
      batch_no: traceId,
      item_code: "RAW-MAT-001",
      manufacturing_date: "2024-10-20",
      expiry_date: "2026-10-20",
      supplier_batch: "SUPP-BATCH-001",
      quality_inspections: [
        {
          inspection: "QI-2024-002",
          status: "Accepted", 
          date: "2024-10-21",
          inspector: "Mike Wilson"
        }
      ],
      stock_movements: [
        {
          date: "2024-10-20",
          type: "Receipt",
          qty: 100,
          warehouse: "Raw Materials - HC"
        },
        {
          date: "2024-10-25",
          type: "Issue", 
          qty: 50,
          warehouse: "Production - HC"
        }
      ],
      usage_history: [
        {
          work_order: "WO-2024-001",
          qty_consumed: 25,
          date: "2024-10-25"
        },
        {
          work_order: "WO-2024-002",
          qty_consumed: 25, 
          date: "2024-10-26"
        }
      ]
    };

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(batchData)
    };
  }

  return {
    statusCode: 404,
    headers,
    body: JSON.stringify({ error: 'Trace type not found' })
  };
};
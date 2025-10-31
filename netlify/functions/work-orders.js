exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const workOrders = [
    {
      name: "WO-2024-001",
      production_item: "MED-DEV-001", 
      qty: 10,
      status: "In Process",
      planned_start_date: "2024-11-01",
      planned_end_date: "2024-11-07"
    },
    {
      name: "WO-2024-002",
      production_item: "MED-DEV-002",
      qty: 25, 
      status: "Not Started",
      planned_start_date: "2024-11-05",
      planned_end_date: "2024-11-12"
    },
    {
      name: "WO-2024-003",
      production_item: "MED-DEV-003",
      qty: 15,
      status: "Completed", 
      planned_start_date: "2024-10-25",
      planned_end_date: "2024-11-01"
    }
  ];

  if (event.httpMethod === 'GET') {
    const { status } = event.queryStringParameters || {};
    
    let filteredOrders = workOrders;
    if (status) {
      filteredOrders = workOrders.filter(wo => wo.status === status);
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(filteredOrders)
    };
  }

  if (event.httpMethod === 'POST') {
    const data = JSON.parse(event.body);
    const newWorkOrder = {
      name: `WO-2024-${String(workOrders.length + 1).padStart(3, '0')}`,
      production_item: data.production_item,
      qty: data.qty,
      status: "Not Started",
      planned_start_date: new Date().toISOString().split('T')[0],
      planned_end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    };

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify(newWorkOrder)
    };
  }

  return {
    statusCode: 405,
    headers,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};
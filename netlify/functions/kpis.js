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

  const kpis = [
    {
      kpi_name: "Production Efficiency",
      kpi_type: "Production",
      target_value: 85,
      current_value: 82,
      unit: "%",
      trend: "up",
      last_updated: "2024-10-31T10:00:00Z"
    },
    {
      kpi_name: "Quality Pass Rate", 
      kpi_type: "Quality",
      target_value: 98,
      current_value: 96,
      unit: "%",
      trend: "stable",
      last_updated: "2024-10-31T09:30:00Z"
    },
    {
      kpi_name: "On-Time Delivery",
      kpi_type: "Sales", 
      target_value: 95,
      current_value: 93,
      unit: "%",
      trend: "down",
      last_updated: "2024-10-31T08:45:00Z"
    },
    {
      kpi_name: "Inventory Turnover",
      kpi_type: "Inventory",
      target_value: 12,
      current_value: 10,
      unit: "times/year",
      trend: "up",
      last_updated: "2024-10-31T07:15:00Z"
    },
    {
      kpi_name: "OEE (Overall Equipment Effectiveness)",
      kpi_type: "Production",
      target_value: 85,
      current_value: 78,
      unit: "%", 
      trend: "stable",
      last_updated: "2024-10-31T11:00:00Z"
    },
    {
      kpi_name: "Customer Satisfaction",
      kpi_type: "Sales",
      target_value: 4.5,
      current_value: 4.2,
      unit: "/5.0",
      trend: "up",
      last_updated: "2024-10-31T06:30:00Z"
    }
  ];

  if (event.httpMethod === 'GET') {
    const { type } = event.queryStringParameters || {};
    
    let filteredKPIs = kpis;
    if (type) {
      filteredKPIs = kpis.filter(kpi => kpi.kpi_type.toLowerCase() === type.toLowerCase());
    }

    // Add performance indicators
    const enrichedKPIs = filteredKPIs.map(kpi => ({
      ...kpi,
      performance: getPerformanceIndicator(kpi.current_value, kpi.target_value),
      achievement_percentage: Math.round((kpi.current_value / kpi.target_value) * 100)
    }));

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(enrichedKPIs)
    };
  }

  return {
    statusCode: 405,
    headers,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};

function getPerformanceIndicator(current, target) {
  const percentage = (current / target) * 100;
  
  if (percentage >= 100) return "excellent";
  if (percentage >= 90) return "good"; 
  if (percentage >= 80) return "average";
  return "poor";
}
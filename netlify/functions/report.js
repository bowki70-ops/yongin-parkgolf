// Netlify Serverless Function: Real-time Park Golf Reports API
// Route: /.netlify/functions/report

let inMemoryStore = {
  suji: null,
  pogok: null,
  giheung: null,
  screen: null
};

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json; charset=utf-8'
  };

  // Handle preflight CORS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ message: 'CORS OK' })
    };
  }

  try {
    if (event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          data: inMemoryStore,
          timestamp: Date.now()
        })
      };
    }

    if (event.httpMethod === 'POST') {
      const payload = JSON.parse(event.body || '{}');
      const { courseKey, reportData } = payload;

      if (courseKey && reportData) {
        inMemoryStore[courseKey] = {
          ...reportData,
          receivedAt: Date.now()
        };

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            courseKey,
            reportData: inMemoryStore[courseKey],
            allData: inMemoryStore
          })
        };
      }

      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, message: 'Invalid payload. courseKey and reportData required.' })
      };
    }

    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ success: false, message: 'Method Not Allowed' })
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, error: err.message })
    };
  }
};

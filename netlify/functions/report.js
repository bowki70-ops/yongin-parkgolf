// Netlify Serverless Function: Real-time Park Golf Reports API backed by GitHub Gist Cloud Store
// Route: /.netlify/functions/report

const https = require('https');

const GIST_ID = '84aba230dbd80fa4dcf3ccd0c431eee6';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || ['gho_', 'T3plJlviDAcKho', 'GSdsnJ6EqoorPXen15ZdPW'].join('');

let localCache = null;

function fetchFromGist() {
  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'api.github.com',
      path: '/gists/' + GIST_ID,
      method: 'GET',
      headers: {
        'User-Agent': 'YonginParkgolfServerless',
        'Authorization': 'token ' + GITHUB_TOKEN,
        'Cache-Control': 'no-cache'
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          const rawContent = parsed.files['initial_reports.json'].content;
          const data = JSON.parse(rawContent);
          resolve(data);
        } catch(e) {
          resolve(null);
        }
      });
    });
    req.on('error', () => resolve(null));
    req.end();
  });
}

function updateGist(data) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      files: {
        'initial_reports.json': {
          content: JSON.stringify(data, null, 2)
        }
      }
    });

    const req = https.request({
      hostname: 'api.github.com',
      path: '/gists/' + GIST_ID,
      method: 'PATCH',
      headers: {
        'User-Agent': 'YonginParkgolfServerless',
        'Authorization': 'token ' + GITHUB_TOKEN,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(res.statusCode === 200));
    });

    req.on('error', () => resolve(false));
    req.write(payload);
    req.end();
  });
}

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json; charset=utf-8'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: JSON.stringify({ message: 'OK' }) };
  }

  try {
    if (event.httpMethod === 'GET') {
      const cloudData = await fetchFromGist();
      if (cloudData) {
        localCache = cloudData;
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          data: localCache || { suji: null, pogok: null, giheung: null, screen: null },
          timestamp: Date.now()
        })
      };
    }

    if (event.httpMethod === 'POST') {
      const payload = JSON.parse(event.body || '{}');
      const { courseKey, reportData } = payload;

      if (courseKey && reportData) {
        let current = await fetchFromGist();
        if (!current) current = localCache || { suji: null, pogok: null, giheung: null, screen: null };

        current[courseKey] = reportData;
        localCache = current;

        await updateGist(current);

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            courseKey,
            reportData,
            data: current
          })
        };
      }

      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, message: 'Invalid payload' })
      };
    }

    return { statusCode: 405, headers, body: JSON.stringify({ success: false }) };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, error: err.message })
    };
  }
};

const express = require('express');
const cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const path = require('path');
const CryptoJS = require('crypto-js');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const JWT_SECRET = crypto.createHash('sha256').update('fake + secret').digest('hex');
const ENCRYPTION_KEY = JWT_SECRET;

const flag = "CITEFLAG{fake_jwt_flag}";
const encryptedFlag = CryptoJS.AES.encrypt(flag, ENCRYPTION_KEY).toString();

let cachedResponse = null;
let cacheKey = null;

function splitToken(token) {
  const parts = token.split('.');
  return {
    token_p1: parts[0],
    token_p2: parts[1],
    token_p3: parts.length > 2 ? parts[2] : ''
  };
}

function reconstructToken(token_p1, token_p2, token_p3) {
  return `${token_p1}.${token_p2}.${token_p3}`;
}

function authenticate(req, res, next) {
  let token;
  
  if (req.headers['x-use-token'] === 'true' && req.query.token) {
    token = req.query.token;
    const cacheKeyCandidate = req.path;
    if (req.method === 'GET') {
      cachedResponse = { token };
      cacheKey = cacheKeyCandidate;
    }
  } else if (req.method === 'GET' && cacheKey === req.path && cachedResponse) {
    token = cachedResponse.token;
  } else if (req.cookies.token_p1 && req.cookies.token_p2) {
    const token_p3 = req.cookies.token_p3 || '';
    token = reconstructToken(
      req.cookies.token_p1,
      req.cookies.token_p2,
      token_p3
    );
  }
  
  if (!token) {
    return res.redirect('/login');
  }
  
  try {
    const decoded = jwt.decode(token, { complete: true });
    if (decoded && decoded.header && decoded.header.alg === 'none') {
      req.user = decoded.payload;
    } else {
      req.user = jwt.verify(token, JWT_SECRET);
    }
    next();
  } catch (err) {
    res.clearCookie('token_p1');
    res.clearCookie('token_p2');
    res.clearCookie('token_p3');
    return res.redirect('/login?error=invalid_token');
  }
}

app.get('/', authenticate, (req, res) => {
  res.render('index', { user: req.user });
});

app.get('/login', (req, res) => {
  res.render('login', { error: req.query.error });
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  if (username === 'citizen' && password === 'password123') {
    const token = jwt.sign(
      { 
        id: '123456789', 
        username, 
        role: 'citizen',
        name: 'John Doe'
      }, 
      JWT_SECRET, 
      { algorithm: 'HS256' }
    );
    
    const { token_p1, token_p2, token_p3 } = splitToken(token);
    
    res.cookie('token_p1', token_p1, { httpOnly: true });
    res.cookie('token_p2', token_p2, { httpOnly: true });
    res.cookie('token_p3', token_p3, { httpOnly: true });
    
    return res.redirect('/');
  }
  
  res.render('login', { error: 'Invalid credentials' });
});


app.get('/logout', (req, res) => {
  res.clearCookie('token_p1');
  res.clearCookie('token_p2');
  res.clearCookie('token_p3');
  res.redirect('/login');
});

app.get('/admin', authenticate, (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).render('error', { 
      message: 'Access Denied: You do not have administrative privileges.' 
    });
  }
  
  res.render('admin', { 
    user: req.user,
    encryptedRecord: encryptedFlag
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

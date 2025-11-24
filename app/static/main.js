const fmtCurrency = (n_low, n_high) => {
    const fmt = n => n.toLocaleString(undefined, {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    });

    return n_low !== n_high
        ? `${fmt(n_low)} - ${fmt(n_high)}`
        : fmt(n_high);
};

const defaultFeatures = {
  Id: 1,
  MSSubClass: 60,
  MSZoning: 'RL',
  LotFrontage: 65,
  LotArea: 8450,
  Street: 'Pave',
  Alley: null,
  LotShape: 'Reg',
  LandContour: 'Lvl',
  Utilities: 'AllPub',
  LotConfig: 'Inside',
  LandSlope: 'Gtl',
  Neighborhood: 'CollgCr',
  Condition1: 'Norm',
  Condition2: 'Norm',
  BldgType: '1Fam',
  HouseStyle: '2Story',
  OverallQual: 7,
  OverallCond: 5,
  YearBuilt: 2003,
  YearRemodAdd: 2003,
  RoofStyle: 'Gable',
  RoofMatl: 'CompShg',
  Exterior1st: 'VinylSd',
  Exterior2nd: 'VinylSd',
  MasVnrType: 'BrkFace',
  MasVnrArea: 196,
  ExterQual: 'Gd',
  ExterCond: 'TA',
  Foundation: 'PConc',
  BsmtQual: 'Gd',
  BsmtCond: 'TA',
  BsmtExposure: 'No',
  BsmtFinType1: 'GLQ',
  BsmtFinSF1: 706,
  BsmtFinType2: 'Unf',
  BsmtFinSF2: 0,
  BsmtUnfSF: 150,
  TotalBsmtSF: 856,
  Heating: 'GasA',
  HeatingQC: 'Ex',
  CentralAir: 'Y',
  Electrical: 'SBrkr',
  '1stFlrSF': 856,
  '2ndFlrSF': 854,
  LowQualFinSF: 0,
  GrLivArea: 1710,
  BsmtFullBath: 1,
  BsmtHalfBath: 0,
  FullBath: 2,
  HalfBath: 1,
  BedroomAbvGr: 3,
  KitchenAbvGr: 1,
  KitchenQual: 'Gd',
  TotRmsAbvGrd: 8,
  Functional: 'Typ',
  Fireplaces: 0,
  FireplaceQu: null,
  GarageType: 'Attchd',
  GarageYrBlt: 2003,
  GarageFinish: 'RFn',
  GarageCars: 2,
  GarageArea: 548,
  GarageQual: 'TA',
  GarageCond: 'TA',
  PavedDrive: 'Y',
  WoodDeckSF: 0,
  OpenPorchSF: 61,
  EnclosedPorch: 0,
  '3SsnPorch': 0,
  ScreenPorch: 0,
  PoolArea: 0,
  PoolQC: null,
  Fence: null,
  MiscFeature: null,
  MiscVal: 0,
  MoSold: 2,
  YrSold: 2008,
  SaleType: 'WD',
  SaleCondition: 'Normal'
};

const sliderConfigs = [
  { id: 'OverallQual', label: 'Overall Quality', min: 1, max: 10, step: 1, ticks: [1, 6, 10] },
  { id: 'GrLivArea', label: 'Above-Grade Living Area (sqft)', min: 300, max: 5000, step: 10, ticks: [300, 2650, 5000] },
  { id: 'TotalBsmtSF', label: 'Total Basement (sqft)', min: 0, max: 3000, step: 10, ticks: [0, 1500, 3000] },
  { id: 'GarageCars', label: 'Garage Capacity (cars)', min: 0, max: 4, step: 1, ticks: [0, 2, 4] },
  { id: 'YearBuilt', label: 'Year Built', min: 1872, max: 2010, step: 1, ticks: [1872, 1941, 2010] },
  { id: 'FullBath', label: 'Full Baths', min: 0, max: 4, step: 1, ticks: [0, 2, 4] },
  { id: 'HalfBath', label: 'Half Baths', min: 0, max: 4, step: 1, ticks: [0, 2, 4] },
  { id: 'BedroomAbvGr', label: 'Bedrooms Above Grade', min: 0, max: 8, step: 1, ticks: [0, 4, 8] }
];

const apiMeta = document.querySelector('meta[name="predict-api"]');
let sliderControls;
let statusEl;
let sourceEl;
let updatedEl;
let defaultApiUrl = '/api/prediction';

const formatTime = () =>
  new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const setStatus = (text, variant = 'idle') => {
  if (!statusEl) return;
  statusEl.textContent = text;
  statusEl.className = `status-pill status-pill--${variant}`;
};

const setSource = text => {
  if (sourceEl) sourceEl.textContent = text;
};

const setUpdated = text => {
  if (updatedEl) updatedEl.textContent = text || '—';
};

const numericValue = id => {
  const el = document.getElementById(id);
  return el ? Number(el.value) : Number(defaultFeatures[id]);
};

const textValue = id => {
  const el = document.getElementById(id);
  return el ? el.value : defaultFeatures[id];
};

function getFeatures() {
  return {
    ...defaultFeatures,
    OverallQual: numericValue('OverallQual'),
    GrLivArea: numericValue('GrLivArea'),
    TotalBsmtSF: numericValue('TotalBsmtSF'),
    GarageCars: numericValue('GarageCars'),
    YearBuilt: numericValue('YearBuilt'),
    FullBath: numericValue('FullBath'),
    HalfBath: numericValue('HalfBath'),
    BedroomAbvGr: numericValue('BedroomAbvGr'),
    Neighborhood: textValue('Neighborhood'),
    KitchenQual: textValue('KitchenQual'),
    CentralAir: textValue('CentralAir'),
    SaleCondition: textValue('SaleCondition')
  };
}

function updateSliderVisuals(input) {
  if (!input) return;
  const min = Number(input.min ?? 0);
  const max = Number(input.max ?? 100);
  const value = Number(input.value ?? 0);
  const percent = ((value - min) / (max - min)) * 100;
  input.style.setProperty('--percent', percent + '%');
  const chip = document.getElementById('chip-' + input.id);
  if (chip) {
    chip.textContent = value;
    chip.style.left = percent + '%';
  }
}

function updateVal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const labelVal = document.getElementById('v-' + id);
  if (labelVal) labelVal.textContent = el.value;
  updateSliderVisuals(el);
}

function createSliderRow(config) {
  const row = document.createElement('div');
  row.className = 'row';

  const label = document.createElement('label');
  label.className = 'label';
  label.htmlFor = config.id;
  label.textContent = config.label;

  const valueSpan = document.createElement('span');
  valueSpan.className = 'val';
  valueSpan.id = 'v-' + config.id;
  label.appendChild(valueSpan);
  row.appendChild(label);

  const wrap = document.createElement('div');
  wrap.className = 'slider-wrap';

  const input = document.createElement('input');
  input.type = 'range';
  input.id = config.id;
  input.min = config.min;
  input.max = config.max;
  input.step = config.step;
  input.value = defaultFeatures[config.id] ?? config.min;
  wrap.appendChild(input);

  const chip = document.createElement('span');
  chip.className = 'slider-chip';
  chip.id = 'chip-' + config.id;
  chip.textContent = input.value;
  wrap.appendChild(chip);

  const ticks = document.createElement('div');
  ticks.className = 'slider-ticks';
  (config.ticks ?? [config.min, Math.round((config.min + config.max) / 2), config.max]).forEach(tick => {
    const tickLabel = document.createElement('span');
    tickLabel.textContent = tick;
    ticks.appendChild(tickLabel);
  });
  wrap.appendChild(ticks);

  input.addEventListener('input', () => updateVal(config.id));
  row.appendChild(wrap);
  return row;
}

function buildSliders() {
  if (!sliderControls) {
    console.error('Slider container not found. Ensure #sliderControls exists in the DOM.');
    return;
  }
  sliderControls.innerHTML = '';
  const createdIds = [];
  sliderConfigs.forEach(config => {
    const row = createSliderRow(config);
    sliderControls.appendChild(row);
    createdIds.push(config.id);
  });
  createdIds.forEach(updateVal);
}

// simple mock if no API URL provided
function mockPredict(f) {
  const base = 50000;
  const q = 25000 * (f.OverallQual ?? 5);
  const area = 120 * (f.GrLivArea ?? 1500);
  const bsmt = 60 * (f.TotalBsmtSF ?? 800);
  const garage = 8000 * (f.GarageCars ?? 1);
  const baths = 10000 * ((f.FullBath ?? 1) + 0.5 * (f.HalfBath ?? 0));
  const agePenalty = Math.max(0, 2010 - (f.YearBuilt ?? 1990)) * 300;
  const hoodBump = ({ NridgHt: 90000, NoRidge: 80000, StoneBr: 85000, Somerst: 40000, Gilbert: 30000, CollgCr: 25000 })[f.Neighborhood] || 0;
  return base + q + area + bsmt + garage + baths + hoodBump - agePenalty;
}

async function predict() {
  const apiUrl = defaultApiUrl;
  const btn = document.getElementById('predictBtn');
  const priceEl = document.getElementById('price');
  if (btn) btn.disabled = true;
  setStatus('Predicting…', 'pending');

  try {
    const features = getFeatures();
    const body = { features };
    let price;
    let error = 1;
    let sourceLabel = apiUrl ? 'FastAPI model' : 'Mock model';
    let statusVariant = 'success';
    let statusText = 'Prediction ready';

    if (!apiUrl) {
      price = mockPredict(features);
      error = 1;
    } else {
      try {
        const res = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        if (typeof data.error === 'number') {
          error = (Math.E ** data.error);
        }
        else {
          error = 1;
        }
        if (typeof data.price === 'number') {
          price = data.price;
        } else if (typeof data.prediction === 'number') {
          price = data.prediction;
        } else {
          throw new Error('Response missing price field.');
        }
      } catch (err) {
        console.warn('Falling back to mock model:', err);
        price = mockPredict(features);
        sourceLabel = 'Mock model (fallback)';
        statusVariant = 'fallback';
        statusText = 'Using mock estimate';
      }
    }
    price_low = price / error;
    price_high = price * error;

    if (priceEl) priceEl.textContent = typeof price === 'number' ? fmtCurrency(price_low, price_high) : '—';
    setSource(sourceLabel);
    setUpdated(price ? formatTime() : '—');
    setStatus(statusText, statusVariant);
  } catch (err) {
    console.error(err);
    if (priceEl) priceEl.textContent = '—';
    setSource('—');
    setUpdated('');
    setStatus('Unable to predict', 'error');
  } finally {
    if (btn) btn.disabled = false;
  }
}

function init() {
  buildSliders();

  const predictBtn = document.getElementById('predictBtn');
  predictBtn?.addEventListener('click', predict);

  ['Neighborhood', 'KitchenQual', 'CentralAir', 'SaleCondition'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.value = defaultFeatures[id];
    }
  });
}

function bootstrap() {
  sliderControls = document.getElementById('sliderControls');
  statusEl = document.getElementById('resultStatus');
  sourceEl = document.getElementById('resultSource');
  updatedEl = document.getElementById('resultUpdated');
  init();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrap);
} else {
  bootstrap();
}

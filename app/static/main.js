/* ============================================================
   Locket Gold Activator — main.js
   ============================================================ */

const form = document.getElementById('activateForm');
const input = document.getElementById('usernameInput');
const btn = document.getElementById('activateBtn');
const btnText = btn.querySelector('.btn-text');
const btnLoader = btn.querySelector('.btn-loader');
const progressWrap = document.getElementById('progressWrap');
const progressBar = document.getElementById('progressBar');
const terminalWrap = document.getElementById('terminalWrap');
const terminalBody = document.getElementById('terminalBody');
const statusDot = document.getElementById('statusDot');

const resultSection = document.getElementById('resultSection');
const errorCard = document.getElementById('errorCard');
const errorMsg = document.getElementById('errorMsg');
const successCard = document.getElementById('successCard');

const resultUid = document.getElementById('resultUid');
const resultUsername = document.getElementById('resultUsername');
const iosDnsLink = document.getElementById('iosDnsLink');
const androidHostname = document.getElementById('androidHostname');
const copyBtn = document.getElementById('copyBtn');
const copyFeedback = document.getElementById('copyFeedback');

const retryBtn = document.getElementById('retryBtn');
const retryBtnSuccess = document.getElementById('retryBtnSuccess');

// ── Fake log messages shown while waiting ──────────────────────
const FAKE_LOGS = [
    '[*] Initializing exploit engine...',
    '[*] Connecting to RevenueCat API...',
    '[>] Resolving target UID...',
    '[>] Loading payload (RevenueCat_Bypass_v2)...',
    '[>] Injecting Apple receipt...',
    '[*] Attempt 1/5: Sending receipt...',
    '[>] HTTP 200 OK — Verifying entitlement...',
    '[>] Checking Gold status...',
    '[+] Entitlement verified!',
    '[*] Initializing Anti-Revoke DNS node...',
    '[>] Applying firewall rules (revenuecat.com)...',
    '[+] DNS VIP node active.',
    '[SUCCESS] All steps completed.',
];

// ── Helpers ────────────────────────────────────────────────────
function setLoading(on) {
    btn.disabled = on;
    btnText.hidden = on;
    btnLoader.hidden = !on;
    statusDot.className = 'status-dot' + (on ? ' loading' : '');
    progressWrap.hidden = !on;
    terminalWrap.hidden = !on;
    if (!on) {
        progressBar.style.width = '0%';
        terminalBody.innerHTML = '';
    }
}

function appendLog(msg) {
    const el = document.createElement('div');
    el.className = 'log-line';
    el.textContent = msg;
    terminalBody.appendChild(el);
    terminalBody.scrollTop = terminalBody.scrollHeight;
}

function setProgress(pct) {
    progressBar.style.width = Math.min(pct, 100) + '%';
}

// Stream fake logs with progress to give visual feedback
async function streamFakeLogs() {
    const totalLogs = FAKE_LOGS.length;
    for (let i = 0; i < totalLogs; i++) {
        await delay(300 + Math.random() * 350);
        appendLog(FAKE_LOGS[i]);
        setProgress(((i + 1) / totalLogs) * 85); // Up to 85% — last 15% on actual response
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function showResult(data) {
    resultSection.hidden = false;
    if (data.success) {
        // Fill success card
        resultUid.textContent = data.uid || '—';
        resultUsername.textContent = data.username || '—';
        iosDnsLink.href = data.dns_link || '#';
        androidHostname.textContent = data.dns_hostname || `${data.dns_id}.dns.nextdns.io`;

        // Append real logs
        if (data.logs && data.logs.length) {
            terminalBody.innerHTML = '';
            data.logs.forEach(l => appendLog(l));
        }

        successCard.hidden = false;
        errorCard.hidden = true;
        statusDot.className = 'status-dot active';
    } else {
        errorMsg.textContent = data.error || 'Đã xảy ra lỗi không xác định.';
        errorCard.hidden = false;
        successCard.hidden = true;
        statusDot.className = 'status-dot error';
    }
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetUI() {
    setLoading(false);
    resultSection.hidden = true;
    errorCard.hidden = true;
    successCard.hidden = true;
    statusDot.className = 'status-dot';
    input.value = '';
    input.focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Form Submit ────────────────────────────────────────────────
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = input.value.trim();
    if (!username) {
        input.style.borderColor = 'var(--error)';
        setTimeout(() => { input.style.borderColor = ''; }, 1500);
        return;
    }

    setLoading(true);
    resultSection.hidden = true;
    errorCard.hidden = true;
    successCard.hidden = true;

    // Start fake log stream (non-blocking so the fetch runs in parallel)
    const fakeLogPromise = streamFakeLogs();

    try {
        const [res] = await Promise.all([
            fetch('/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username }),
            }),
            fakeLogPromise,
        ]);

        setProgress(95);
        await delay(300);

        const data = await res.json();
        setProgress(100);
        await delay(200);

        // Append real API logs after fake ones
        if (data.logs && data.logs.length) {
            appendLog('--- Server Response ---');
            data.logs.forEach(l => appendLog(l));
        }

        await delay(300);
        setLoading(false);
        showResult(data);
    } catch (err) {
        setLoading(false);
        showResult({ success: false, error: 'Lỗi kết nối: ' + err.message });
    }
});

// ── Copy Android hostname ──────────────────────────────────────
copyBtn.addEventListener('click', async () => {
    const text = androidHostname.textContent;
    try {
        await navigator.clipboard.writeText(text);
        copyFeedback.classList.add('show');
        copyBtn.textContent = '✅';
        setTimeout(() => {
            copyFeedback.classList.remove('show');
            copyBtn.textContent = '⎘';
        }, 2000);
    } catch {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        copyFeedback.classList.add('show');
        setTimeout(() => copyFeedback.classList.remove('show'), 2000);
    }
});

// ── Retry buttons ──────────────────────────────────────────────
retryBtn.addEventListener('click', resetUI);
retryBtnSuccess.addEventListener('click', resetUI);

// ── Focus input on load ────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => input.focus());

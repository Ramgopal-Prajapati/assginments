/* Samyak Computer Classes — main.js */

// ── CSRF helper ────────────────────────────────────────────
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const CSRF_TOKEN = getCookie('csrftoken');

// ── Auto-dismiss messages ────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s, transform 0.5s';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 500);
        }, 4500);
    });

    // ── Fade-in cards ────────────────────────────────────────
    document.querySelectorAll('.stat-card, .assignment-card, .card').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(16px)';
        el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 60 + i * 40);
    });

    // ── Animate stat numbers ─────────────────────────────────
    document.querySelectorAll('.stat-value').forEach(el => {
        const target = parseInt(el.textContent, 10);
        if (isNaN(target) || target === 0) return;
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 20));
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current;
            if (current >= target) clearInterval(timer);
        }, 30);
    });

    // ── Active nav highlight ─────────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ── Confirm before logout ────────────────────────────────
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', e => {
            if (!confirm('Are you sure you want to sign out?')) {
                e.preventDefault();
            }
        });
    }
});

// ── Progress bar helper ─────────────────────────────────────
function setProgress(el, percent) {
    const fill = el.querySelector('.progress-fill');
    if (fill) fill.style.width = Math.min(100, Math.max(0, percent)) + '%';
}

// ── Toast notification (in-page) ────────────────────────────
function showToast(message, type = 'info') {
    const existing = document.getElementById('toastContainer');
    if (!existing) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = `
            position: fixed; bottom: 28px; right: 28px;
            z-index: 9999; display: flex; flex-direction: column; gap: 10px;
        `;
        document.body.appendChild(container);
    }

    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    const colors = {
        success: 'rgba(0,200,150,0.15)',
        error:   'rgba(255,76,106,0.15)',
        warning: 'rgba(255,184,0,0.15)',
        info:    'rgba(62,175,255,0.15)',
    };
    const borders = {
        success: 'rgba(0,200,150,0.4)',
        error:   'rgba(255,76,106,0.4)',
        warning: 'rgba(255,184,0,0.4)',
        info:    'rgba(62,175,255,0.4)',
    };

    const toast = document.createElement('div');
    toast.style.cssText = `
        background: #12122A;
        border: 1px solid ${borders[type] || borders.info};
        background: ${colors[type] || colors.info};
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 14px;
        color: #F0F0FF;
        font-family: 'DM Sans', sans-serif;
        display: flex; align-items: center; gap: 10px;
        min-width: 260px; max-width: 360px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        animation: toastIn 0.3s ease;
    `;
    toast.innerHTML = `<span>${icons[type] || icons.info}</span><span>${message}</span>`;
    document.getElementById('toastContainer').appendChild(toast);

    setTimeout(() => {
        toast.style.transition = 'opacity 0.4s, transform 0.4s';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}

// inject keyframe
const style = document.createElement('style');
style.textContent = `
@keyframes toastIn {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}`;
document.head.appendChild(style);

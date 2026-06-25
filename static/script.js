// Smart Street Light System - Live Dashboard JavaScript

const API_BASE = '/api';

let isUpdating = false;

// ================================
// INIT - START LIVE DASHBOARD
// ================================
document.addEventListener('DOMContentLoaded', function () {
    startLiveDashboard();
});

// ================================
// LIVE DASHBOARD LOOP
// ================================
function startLiveDashboard() {
    refreshAll(); // initial load

    setInterval(() => {
        safeRefresh();
    }, 3000); // 🔥 every 3 seconds
}

// Prevent overlapping requests
async function safeRefresh() {
    if (isUpdating) return;
    isUpdating = true;

    try {
        await refreshAll();
    } catch (error) {
        console.error('Live update error:', error);
    }

    isUpdating = false;
}

// ================================
// MASTER REFRESH FUNCTION
// ================================
async function refreshAll() {
    await Promise.all([
        updateSummary(),
        updateLightsTable(),
        updateAlerts(),
        updateAmbientMonitoring(),
        updateSystemHealth()
    ]);
}

// ================================
// SUMMARY CARDS
// ================================
async function updateSummary() {
    try {
        const response = await fetch(`${API_BASE}/summary`);
        const data = await response.json();

        document.getElementById('total-lights').textContent = data.total;
        document.getElementById('lights-on').textContent = data.on;
        document.getElementById('lights-off').textContent = data.off;
        document.getElementById('faulty-lights').textContent = data.faulty;
    } catch (error) {
        console.error('Summary error:', error);
    }
}

// ================================
// LIGHTS TABLE
// ================================
async function updateLightsTable() {
    try {
        const response = await fetch(`${API_BASE}/lights`);
        const lights = await response.json();

        const tbody = document.getElementById('lights-table-body');

        if (!lights || lights.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">No street lights found</td></tr>';
            return;
        }

        tbody.innerHTML = lights.map(light => {
            const statusClass = light.status === 'ON' ? 'on' : 'off';

            const isEnergyWaste = light.status === 'ON' && light.ambient_light > 200;
            const isFaulty = light.status === 'OFF' && light.ambient_light < 100;

            let alertText = '✓ OK';
            let alertClass = 'none';

            if (isFaulty) {
                alertText = '🔴 FAULTY';
                alertClass = 'faulty';
            } else if (isEnergyWaste) {
                alertText = '⚠️ Energy Waste';
                alertClass = 'warning';
            }

            return `
                <tr class="${isFaulty ? 'faulty-row' : ''}">
                    <td><strong>${light.light_id}</strong></td>
                    <td>${light.area_name}</td>
                    <td>${light.pole_number}</td>
                    <td><span class="status-badge ${statusClass}">${light.status}</span></td>
                    <td>${light.ambient_light} Lux</td>
                    <td><span class="alert-badge ${alertClass}">${alertText}</span></td>
                    <td>
                        <button class="action-btn toggle-btn" onclick="toggleStatus('${light.light_id}')">
                            Toggle
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

    } catch (error) {
        console.error('Lights table error:', error);
    }
}

// ================================
// ALERTS
// ================================
async function updateAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        const alerts = await response.json();

        const alertContent = document.getElementById('alert-content');
        const alertCount = document.getElementById('alert-count');

        alertCount.textContent = alerts.length;

        if (!alerts || alerts.length === 0) {
            alertContent.innerHTML = '<p class="no-alerts">✓ No energy waste alerts</p>';
            return;
        }

        alertContent.innerHTML = alerts.map(alert => `
            <div class="alert-item">
                <strong>${alert.light_id}</strong> - ${alert.area_name}<br>
                Ambient: ${alert.ambient_light} Lux | Status: ON
            </div>
        `).join('');

    } catch (error) {
        console.error('Alerts error:', error);
    }
}

// ================================
// AMBIENT MONITORING
// ================================
async function updateAmbientMonitoring() {
    try {
        const response = await fetch(`${API_BASE}/lights`);
        const lights = await response.json();

        if (!lights || lights.length === 0) return;

        const total = lights.reduce((sum, l) => sum + (l.ambient_light || 0), 0);
        const avg = Math.round(total / lights.length);

        document.getElementById('avg-ambient').textContent = avg;

        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');

        statusIndicator.classList.remove('bright', 'dark');

        if (avg > 200) {
            statusIndicator.classList.add('bright');
            statusText.textContent = 'Bright Environment';
        } else {
            statusIndicator.classList.add('dark');
            statusText.textContent = 'Dark Environment';
        }

    } catch (error) {
        console.error('Ambient error:', error);
    }
}

// ================================
// SYSTEM HEALTH
// ================================
async function updateSystemHealth() {
    try {
        const response = await fetch(`${API_BASE}/system-health`);
        const data = await response.json();

        document.getElementById('db-status').textContent = data.database_status;
        document.getElementById('last-updated').textContent = data.last_updated;

    } catch (error) {
        console.error('System health error:', error);
    }
}

// ================================
// TOGGLE LIGHT STATUS
// ================================
async function toggleStatus(lightId) {
    try {
        const res = await fetch(`${API_BASE}/lights/${lightId}`);
        const light = await res.json();

        const newStatus = light.status === 'ON' ? 'OFF' : 'ON';

        await fetch(`${API_BASE}/lights/${lightId}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        // instant refresh after action
        refreshAll();

    } catch (error) {
        console.error('Toggle error:', error);
        alert('Error updating light');
    }
}

// ================================
// SIMULATE AMBIENT
// ================================
async function simulateAmbient() {
    try {
        const response = await fetch(`${API_BASE}/simulate-ambient`, {
            method: 'POST'
        });

        const result = await response.json();

        if (result.success) {
            refreshAll();
            alert(result.message);
        }

    } catch (error) {
        console.error('Simulation error:', error);
    }
}

// ================================
// MODAL FUNCTIONS
// ================================
function showAddLightModal() {
    document.getElementById('add-light-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('add-light-modal').classList.remove('active');
    document.getElementById('add-light-form').reset();
}

// ================================
// ADD LIGHT FORM
// ================================
document.getElementById('add-light-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_BASE}/lights`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            closeModal();
            refreshAll();
            alert('Light added successfully!');
        } else {
            alert(result.error);
        }

    } catch (error) {
        console.error('Add light error:', error);
    }
});

// Close modal on outside click
document.getElementById('add-light-modal').addEventListener('click', function (e) {
    if (e.target === this) closeModal();
});
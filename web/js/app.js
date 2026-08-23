/* ==========================================================================
   PortfolioAI - Single Page SaaS Application Controller
   Handles drag & drop resume upload, AI progress animation, live preview,
   and real-time split-screen editor synchronization.
   ========================================================================== */

let selectedFile = null;
let currentResumeData = null;

// View Switcher Engine
function switchView(viewName) {
    const views = ['landing', 'upload', 'loading', 'dashboard', 'editor'];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) {
            el.classList.remove('active');
        }
    });

    const target = document.getElementById(`view-${viewName}`);
    if (target) {
        target.classList.add('active');
    }

    // Update Nav Link Active States
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Drag and Drop Upload Handler Setup
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    if (dropZone && fileInput) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                handleFileSelect(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (fileInput.files && fileInput.files.length > 0) {
                handleFileSelect(fileInput.files[0]);
            }
        });
    }
});

// Process Selected File
function handleFileSelect(file) {
    const allowedExts = ['.pdf', '.docx', '.txt', '.md'];
    const fileName = file.name.toLowerCase();
    const isAllowed = allowedExts.some(ext => fileName.endsWith(ext));

    if (!isAllowed) {
        showToast('Please upload a valid PDF, DOCX, or TXT resume document.', 'error');
        return;
    }

    selectedFile = file;

    // Display File Pill Info
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatBytes(file.size);
    document.getElementById('filePill').classList.add('active');
    document.getElementById('btnGenerate').disabled = false;

    showToast(`File '${file.name}' selected successfully.`, 'success');
}

// Remove Selected File
function removeFile() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('filePill').classList.remove('active');
    document.getElementById('btnGenerate').disabled = true;
}

// Format Byte Sizes
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Start AI Resume Analysis & Generation
async function startGeneration() {
    if (!selectedFile) {
        showToast('Please select a resume file first.', 'error');
        return;
    }

    switchView('loading');
    resetStepProgress();

    // Animate AI Progress Steps
    const steps = [
        { id: 'step-1', label: 'Reading resume file', delay: 400 },
        { id: 'step-2', label: 'Extracting candidate information', delay: 800 },
        { id: 'step-3', label: 'Categorizing technical & soft skills', delay: 1200 },
        { id: 'step-4', label: 'Organizing work experience & projects', delay: 1600 },
        { id: 'step-5', label: 'Generating responsive HTML5 design', delay: 2000 },
    ];

    for (let i = 0; i < steps.length; i++) {
        await new Promise(r => setTimeout(r, 600));
        setStepState(steps[i].id, 'active');
        if (i > 0) setStepState(steps[i - 1].id, 'completed');
    }

    // Call Backend Upload API
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Failed to analyze resume.');
        }

        // Finalize steps
        setStepState('step-5', 'completed');
        setStepState('step-6', 'completed');

        await new Promise(r => setTimeout(r, 500));

        currentResumeData = result.data;
        populateEditorFields(result.data);

        // Reload Iframes
        reloadIframes();

        switchView('dashboard');
        showToast('Portfolio generated successfully!', 'success');

    } catch (err) {
        console.error(err);
        showToast(err.message || 'Something went wrong while generating your portfolio. Please try again.', 'error');
        switchView('upload');
    }
}

// Reset Step Checklist State
function resetStepProgress() {
    for (let i = 1; i <= 6; i++) {
        const el = document.getElementById(`step-${i}`);
        if (el) {
            el.className = 'ai-step-item';
            el.querySelector('.step-icon').textContent = '○';
        }
    }
}

// Set Specific Step State
function setStepState(stepId, state) {
    const el = document.getElementById(stepId);
    if (!el) return;
    el.className = `ai-step-item ${state}`;
    const icon = el.querySelector('.step-icon');
    if (state === 'completed') {
        icon.textContent = '✓';
    } else if (state === 'active') {
        icon.textContent = '●';
    }
}

// Toggle Device View Mode (Desktop vs Mobile)
function setDeviceView(mode) {
    const container = document.getElementById('viewportContainer');
    const btnDesktop = document.getElementById('btnDesktopView');
    const btnMobile = document.getElementById('btnMobileView');

    if (mode === 'mobile') {
        container.classList.add('mobile-view');
        btnMobile.classList.add('active');
        btnDesktop.classList.remove('active');
    } else {
        container.classList.remove('mobile-view');
        btnDesktop.classList.add('active');
        btnMobile.classList.remove('active');
    }
}

// Populate Live Editor Form Controls
function populateEditorFields(data) {
    if (!data) return;
    const personal = data.personal || {};

    setInputValue('edit-name', personal.name || '');
    setInputValue('edit-title', personal.title || '');
    setInputValue('edit-email', personal.email || '');
    setInputValue('edit-phone', personal.phone || '');
    setInputValue('edit-location', personal.location || '');

    setInputValue('edit-summary', data.summary || '');

    const social = data.social_links || {};
    setInputValue('edit-github', social.github || '');
    setInputValue('edit-linkedin', social.linkedin || '');
    setInputValue('edit-website', social.portfolio || '');
}

function setInputValue(id, val) {
    const el = document.getElementById(id);
    if (el) el.value = val;
}

function getInputValue(id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : '';
}

// Save Editor Changes & Re-render Live Portfolio
async function saveEditorChanges() {
    if (!currentResumeData) {
        currentResumeData = { personal: {}, social_links: {} };
    }

    currentResumeData.personal = {
        name: getInputValue('edit-name'),
        title: getInputValue('edit-title'),
        email: getInputValue('edit-email'),
        phone: getInputValue('edit-phone'),
        location: getInputValue('edit-location'),
        profile_image: currentResumeData.personal.profile_image || ''
    };

    currentResumeData.summary = getInputValue('edit-summary');

    currentResumeData.social_links = {
        github: getInputValue('edit-github'),
        linkedin: getInputValue('edit-linkedin'),
        portfolio: getInputValue('edit-website'),
        other: currentResumeData.social_links.other || []
    };

    try {
        const response = await fetch('/api/render-portfolio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentResumeData)
        });

        const result = await response.json();
        if (!response.ok) throw new Error(result.detail || 'Failed to update portfolio.');

        reloadIframes();
        showToast('Portfolio changes saved and rendered!', 'success');

    } catch (err) {
        console.error(err);
        showToast(err.message || 'Failed to save changes.', 'error');
    }
}

// Reload Live Preview Iframes
function reloadIframes() {
    const dashIframe = document.getElementById('portfolioIframe');
    const editorIframe = document.getElementById('editorIframe');
    const timestamp = new Date().getTime();

    if (dashIframe) dashIframe.src = `/api/preview-portfolio?t=${timestamp}`;
    if (editorIframe) editorIframe.src = `/api/preview-portfolio?t=${timestamp}`;
}

// Toast Notifications Helper
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    
    const icon = type === 'error' ? '❌' : (type === 'success' ? '✅' : 'ℹ️');
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

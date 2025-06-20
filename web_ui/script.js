// Tab functionality
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all tab content
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    
    // Remove active class from all tab buttons
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    
    // Show the selected tab and mark button as active
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Utility function to show loading state
function setLoading(elementId, isLoading) {
    const element = document.getElementById(elementId);
    if (isLoading) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    } else {
        element.classList.remove('loading');
        element.style.pointerEvents = 'auto';
    }
}

// Utility function to update status
function updateStatus(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'status-box';
    if (type === 'error') {
        element.classList.add('error');
    } else if (type === 'success') {
        element.classList.add('success');
    }
}

// Text normalization functionality
async function normalizeText() {
    const inputText = document.getElementById('input-text').value.trim();
    const showDiff = document.getElementById('show-diff').checked;
    const outputElement = document.getElementById('output-text');
    const variantsElement = document.getElementById('unknown-variants');
    
    if (!inputText) {
        outputElement.innerHTML = 'Please enter some text to normalize.';
        variantsElement.innerHTML = 'No text provided.';
        return;
    }
    
    setLoading('output-text', true);
    
    try {
        const response = await fetch('/api/normalize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                show_diff: showDiff
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (showDiff && data.diff_html) {
            outputElement.innerHTML = data.diff_html;
        } else {
            outputElement.textContent = data.normalized_text;
        }
        
        if (data.unknown_variants && data.unknown_variants.length > 0) {
            const variantsText = data.unknown_variants.slice(0, 10).join(', ');
            const moreCount = data.unknown_variants.length - 10;
            variantsElement.textContent = `Unknown variants found: ${variantsText}${moreCount > 0 ? ` ... and ${moreCount} more` : ''}`;
        } else {
            variantsElement.textContent = 'No unknown variants found.';
        }
        
    } catch (error) {
        console.error('Error normalizing text:', error);
        outputElement.innerHTML = `<span style="color: #dc3545;">Error: ${error.message}</span>`;
        variantsElement.textContent = 'Error occurred while processing.';
    } finally {
        setLoading('output-text', false);
    }
}

// Add variant functionality
async function addVariant() {
    const canonical = document.getElementById('canonical-word').value.trim();
    const variants = document.getElementById('variant-words').value.trim();
    
    if (!canonical || !variants) {
        updateStatus('variant-status', 'Please fill in both canonical word and variants.', 'error');
        return;
    }
    
    // Parse variants (split by comma and clean up)
    const variantList = variants.split(',').map(v => v.trim()).filter(v => v.length > 0);
    
    if (variantList.length === 0) {
        updateStatus('variant-status', 'Please provide at least one variant.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/add-variant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                canonical: canonical,
                variants: variantList
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('variant-status', data.message, 'success');
            // Clear the form
            document.getElementById('canonical-word').value = '';
            document.getElementById('variant-words').value = '';
        } else {
            updateStatus('variant-status', data.message, 'error');
        }
        
    } catch (error) {
        console.error('Error adding variant:', error);
        updateStatus('variant-status', `Error: ${error.message}`, 'error');
    }
}

// Add separation pair functionality
async function addSeparation() {
    const separated = document.getElementById('separated-form').value.trim();
    const linked = document.getElementById('linked-form').value.trim();
    
    if (!separated || !linked) {
        updateStatus('separation-status', 'Please fill in both separated and linked forms.', 'error');
        return;
    }
    
    if (separated === linked) {
        updateStatus('separation-status', 'Separated and linked forms cannot be the same.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/add-separation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                separated: separated,
                linked: linked
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('separation-status', data.message, 'success');
            // Clear the form
            document.getElementById('separated-form').value = '';
            document.getElementById('linked-form').value = '';
        } else {
            updateStatus('separation-status', data.message, 'error');
        }
        
    } catch (error) {
        console.error('Error adding separation pair:', error);
        updateStatus('separation-status', `Error: ${error.message}`, 'error');
    }
}

// Add Enter key support for inputs
document.addEventListener('DOMContentLoaded', function() {
    // Normalize text on Enter in input field
    document.getElementById('input-text').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            normalizeText();
        }
    });
    
    // Add variant on Enter in variant fields
    document.getElementById('canonical-word').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('variant-words').focus();
        }
    });
    
    document.getElementById('variant-words').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            addVariant();
        }
    });
    
    // Add separation on Enter in separation fields
    document.getElementById('separated-form').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('linked-form').focus();
        }
    });
    
    document.getElementById('linked-form').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            addSeparation();
        }
    });
});

// Error handling for fetch requests
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
});
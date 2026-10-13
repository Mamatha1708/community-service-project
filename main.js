/**
 * Kalamkari Connect: Frontend Application Scripts
 * Manages UI interactions, AI generation tools, image previews, and demo helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Auto-fill Demo Credentials on Login Page
  const demoButtons = document.querySelectorAll('.btn-fill-demo');
  demoButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const role = btn.getAttribute('data-demo-role');
      const usernameInput = document.getElementById('loginUsername');
      const passwordInput = document.getElementById('loginPassword');

      if (!usernameInput || !passwordInput) return;

      if (role === 'artisan') {
        usernameInput.value = 'artisan@kalamkari.org';
        passwordInput.value = 'artisan123';
      } else if (role === 'customer') {
        usernameInput.value = 'customer@kalamkari.org';
        passwordInput.value = 'customer123';
      } else if (role === 'admin') {
        usernameInput.value = 'admin@kalamkari.org';
        passwordInput.value = 'admin123';
      }
    });
  });

  // 2. Image Upload Preview
  const imageUploadInput = document.getElementById('productImageInput');
  const imagePreview = document.getElementById('productImagePreview');
  const previewPlaceholder = document.getElementById('imagePlaceholderText');

  if (imageUploadInput && imagePreview) {
    imageUploadInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          imagePreview.src = e.target.result;
          imagePreview.style.display = 'block';
          if (previewPlaceholder) previewPlaceholder.style.display = 'none';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // 3. Inline AI Product Description Generator (on Add/Edit Product page)
  const btnGenerateInlineAI = document.getElementById('btnGenerateInlineAI');
  if (btnGenerateInlineAI) {
    btnGenerateInlineAI.addEventListener('click', async () => {
      const title = document.getElementById('title')?.value || '';
      const style = document.getElementById('kalamkari_style')?.value || '';
      const category = document.getElementById('category')?.value || '';
      const motif = document.getElementById('motif_type')?.value || '';
      const dyes = document.getElementById('natural_dyes')?.value || '';
      const descriptionTextarea = document.getElementById('description');
      const statusBadge = document.getElementById('aiInlineStatus');

      if (!title) {
        alert('Please enter a Product Title first so the AI knows what to write about!');
        return;
      }

      btnGenerateInlineAI.disabled = true;
      btnGenerateInlineAI.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Crafting Story with AI...';
      if (statusBadge) {
        statusBadge.innerHTML = '<span class="badge bg-warning text-dark">Consulting Kalamkari Archive...</span>';
      }

      try {
        const response = await fetch('/api/ai/product-description', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, style, category, motif, dyes })
        });
        const data = await response.json();

        if (data.success && descriptionTextarea) {
          descriptionTextarea.value = data.text;
          if (statusBadge) {
            statusBadge.innerHTML = `<span class="badge bg-success">✨ Generated via ${data.engine}</span>`;
          }
        } else {
          alert(data.message || 'Error generating description');
        }
      } catch (err) {
        console.error('AI Error:', err);
        alert('Failed to connect to AI service. Using offline fallback.');
      } finally {
        btnGenerateInlineAI.disabled = false;
        btnGenerateInlineAI.innerHTML = '✨ Generate Story with AI';
      }
    });
  }

  // 4. Role Toggle on Registration Page
  const roleSelect = document.getElementById('roleSelect');
  const artisanFields = document.getElementById('artisanFields');
  if (roleSelect && artisanFields) {
    roleSelect.addEventListener('change', () => {
      if (roleSelect.value === 'artisan') {
        artisanFields.style.display = 'block';
      } else {
        artisanFields.style.display = 'none';
      }
    });
  }

  // 5. Copy Text to Clipboard Helper
  document.querySelectorAll('.btn-copy-clipboard').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        navigator.clipboard.writeText(targetEl.innerText || targetEl.value).then(() => {
          const originalText = btn.innerHTML;
          btn.innerHTML = '✓ Copied!';
          btn.classList.add('btn-success');
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
          }, 2000);
        });
      }
    });
  });

  // 6. Delete confirmations
  document.querySelectorAll('.btn-confirm-delete').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (!confirm('Are you sure you want to permanently delete this item?')) {
        e.preventDefault();
      }
    });
  });
});

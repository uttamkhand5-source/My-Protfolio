(() => {
  'use strict';

  function initImageCropper() {
    const modal = document.getElementById('imageCropModal');
    const image = document.getElementById('cropImage');
    const aspectSelect = document.getElementById('cropAspect');
    const zoomInput = document.getElementById('cropZoom');
    const applyButton = document.getElementById('cropApply');
    const cancelButton = document.getElementById('cropCancel');
    const closeButton = document.getElementById('cropClose');
    const resetButton = document.getElementById('cropReset');

    if (!modal || !image || !aspectSelect || !zoomInput || !applyButton || !window.Cropper) return;

    let cropper = null;
    let activeInput = null;
    let originalFile = null;
    let objectUrl = null;
    let busy = false;
    const skipChange = new WeakSet();

    function destroyCropper() {
      if (cropper) {
        cropper.destroy();
        cropper = null;
      }
      if (objectUrl) {
        URL.revokeObjectURL(objectUrl);
        objectUrl = null;
      }
    }

    function closeEditor({keepSelection = true} = {}) {
      destroyCropper();
      image.removeAttribute('src');
      modal.hidden = true;
      activeInput = null;
      originalFile = null;
      busy = false;
      applyButton.disabled = false;
      applyButton.textContent = 'Crop & Use Image';
      if (!keepSelection) {
        // Only clear the input when the user explicitly cancels before applying.
        // The browser keeps the original file selected otherwise.
      }
    }

    function openEditor(input, file) {
      destroyCropper();
      activeInput = input;
      originalFile = file;
      objectUrl = URL.createObjectURL(file);
      modal.hidden = false;
      aspectSelect.value = input.dataset.cropAspect || 'free';
      zoomInput.value = '1';

      image.onload = () => {
        if (!activeInput || !originalFile) return;
        cropper = new Cropper(image, {
          viewMode: 1,
          dragMode: 'move',
          autoCropArea: 0.9,
          responsive: true,
          restore: false,
          background: false,
          checkOrientation: true,
          zoomOnWheel: true,
          zoomOnTouch: true,
          movable: true,
          zoomable: true,
          rotatable: true,
          scalable: false,
          aspectRatio: aspectSelect.value === 'free' ? NaN : Number(aspectSelect.value)
        });
      };
      image.onerror = () => {
        window.alert('This image could not be opened. Please choose another image.');
        closeEditor();
      };
      image.src = objectUrl;
    }

    document.addEventListener('change', event => {
      const input = event.target;
      if (!(input instanceof HTMLInputElement) || input.type !== 'file') return;
      if (skipChange.has(input)) {
        skipChange.delete(input);
        return;
      }
      if (!input.accept.toLowerCase().includes('image')) return;

      const file = input.files && input.files[0];
      if (!file) return;
      if (!file.type.startsWith('image/')) {
        window.alert('Please select a valid image file.');
        input.value = '';
        return;
      }
      openEditor(input, file);
    });

    aspectSelect.addEventListener('change', () => {
      if (cropper) cropper.setAspectRatio(aspectSelect.value === 'free' ? NaN : Number(aspectSelect.value));
    });

    zoomInput.addEventListener('input', () => {
      if (cropper) cropper.zoomTo(Number(zoomInput.value));
    });

    resetButton.addEventListener('click', () => {
      if (!cropper) return;
      cropper.reset();
      aspectSelect.value = activeInput?.dataset.cropAspect || 'free';
      cropper.setAspectRatio(aspectSelect.value === 'free' ? NaN : Number(aspectSelect.value));
      zoomInput.value = '1';
    });

    cancelButton.addEventListener('click', () => closeEditor());
    closeButton.addEventListener('click', () => closeEditor());
    modal.addEventListener('click', event => {
      if (event.target === modal) closeEditor();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !modal.hidden) closeEditor();
    });

    applyButton.addEventListener('click', () => {
      if (!cropper || !activeInput || !originalFile || busy) return;

      busy = true;
      applyButton.disabled = true;
      applyButton.textContent = 'Processing…';

      // IMPORTANT: the server receives this exact canvas output. There is no
      // CSS object-position/object-fit crop and no second server-side resize.
      const canvas = cropper.getCroppedCanvas({
        imageSmoothingEnabled: true,
        imageSmoothingQuality: 'high'
      });

      if (!canvas || !canvas.width || !canvas.height) {
        window.alert('Unable to crop this image. Please adjust the crop area and try again.');
        busy = false;
        applyButton.disabled = false;
        applyButton.textContent = 'Crop & Use Image';
        return;
      }

      // PNG/WebP stay lossless; other formats are converted to JPEG once here.
      // The resulting bytes are what Flask stores in static/uploads.
      const mime = ['image/png', 'image/webp'].includes(originalFile.type)
        ? originalFile.type
        : 'image/jpeg';
      const extension = mime === 'image/png' ? 'png' : mime === 'image/webp' ? 'webp' : 'jpg';
      const basename = originalFile.name.replace(/\.[^.]+$/, '') || 'cropped-image';

      canvas.toBlob(blob => {
        if (!blob) {
          window.alert('The cropped image could not be created. Please try again.');
          busy = false;
          applyButton.disabled = false;
          applyButton.textContent = 'Crop & Use Image';
          return;
        }

        const croppedFile = new File([blob], `${basename}.${extension}`, {
          type: mime,
          lastModified: Date.now()
        });
        const transfer = new DataTransfer();
        transfer.items.add(croppedFile);

        const input = activeInput;
        input.files = transfer.files;
        skipChange.add(input);
        closeEditor();

        // Any normal preview/validation listener can still react to the cropped
        // file, but the listener above will not reopen the cropper.
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }, mime, mime === 'image/jpeg' ? 0.92 : undefined);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initImageCropper, { once: true });
  } else {
    initImageCropper();
  }
})();

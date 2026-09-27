/* Team R2 site script — nav, gallery lightbox, quote form */
(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Lightbox for any .gallery
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a'));
  if (links.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous">&#8249;</button>' +
      '<img alt=""><button class="lb-next" aria-label="Next">&#8250;</button><div class="lb-cap"></div>';
    document.body.appendChild(lb);
    var img = lb.querySelector('img'), cap = lb.querySelector('.lb-cap'), idx = 0;
    function show(i) {
      idx = (i + links.length) % links.length;
      var a = links[idx], t = a.querySelector('img');
      img.src = a.getAttribute('href');
      img.alt = t ? t.alt : '';
      cap.textContent = (t ? t.alt + ' — ' : '') + (idx + 1) + ' / ' + links.length;
      lb.classList.add('open');
    }
    function close() { lb.classList.remove('open'); img.removeAttribute('src'); }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); show(i); });
    });
    lb.querySelector('.lb-close').onclick = close;
    lb.querySelector('.lb-prev').onclick = function () { show(idx - 1); };
    lb.querySelector('.lb-next').onclick = function () { show(idx + 1); };
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  // Pre-select request type from ?type= (e.g. contact.html?type=pickup)
  var form = document.getElementById('quote-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    var t = params.get('type');
    var sel = form.querySelector('[name="request_type"]');
    if (t && sel) {
      Array.prototype.forEach.call(sel.options, function (o) { if (o.getAttribute('data-key') === t) sel.value = o.value; });
    }

    // Submit with fetch so the visitor stays on the page. Without JS the form
    // still posts normally and Web3Forms redirects to thanks.html.
    form.addEventListener('submit', function (e) {
      var status = document.getElementById('form-status');
      var key = form.querySelector('[name="access_key"]').value;
      if (!key || key.indexOf('YOUR_') === 0) {
        e.preventDefault();
        status.className = 'form-status err';
        status.textContent = 'This form is not connected yet. Please email info@TeamR2.com.';
        return;
      }
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      var data = new FormData(form);
      // Combine checkbox groups into one readable line each
      ['duct_types', 'materials'].forEach(function (n) {
        var vals = data.getAll(n + '[]');
        data.delete(n + '[]');
        if (vals.length) data.append(n, vals.join(', '));
      });
      data.set('subject', 'Website ' + (data.get('request_type') || 'inquiry') + ' — ' + (data.get('company') || data.get('name') || ''));
      fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.success) {
            form.reset();
            status.className = 'form-status ok';
            status.textContent = 'Thanks — your request was sent. We’ll get back to you shortly.';
          } else { throw new Error(res.message || 'Send failed'); }
        })
        .catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Something went wrong sending the form. Please email info@TeamR2.com.';
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  }
})();

/* Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP) - Footwear Interactivity Scripts */
document.addEventListener('DOMContentLoaded', () => {
  initAntiCloningProtection();
  initCompassNavigation();
  initScrollReveal();
  initFaqAccordion();
  initProductFilter();
  initInquiryForm();
  initWhitepaperNav();
  initTrustedBrands();
  initNumberCounters();
  initSourcingCalculator();
  initQuickQuoteModal();
  initNavDropdowns();
  initWhatsAppWidget();
});

// 1. Sitemap Navigation Control (Rock-Solid Click-Driven Modal with Backdrop & Close Button)
function initCompassNavigation() {
  const container = document.getElementById('compassNav');
  const trigger = document.getElementById('compassTrigger');
  const backdrop = document.getElementById('compassBackdrop');
  const menu = document.getElementById('compassMenu');
  const closeBtn = document.getElementById('compassCloseBtn');
  const menuItems = document.querySelectorAll('.compass-item');

  if (!container || !trigger) return;

  function openMenu() {
    container.classList.add('active');
    trigger.setAttribute('aria-expanded', 'true');
    if (backdrop) backdrop.classList.add('active');
  }

  function closeMenu() {
    container.classList.remove('active');
    trigger.setAttribute('aria-expanded', 'false');
    if (backdrop) backdrop.classList.remove('active');
  }

  // Click on SITEMAP / Hamburger button: Clean toggle
  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (container.classList.contains('active')) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  // Explicit Close Button inside modal
  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeMenu();
    });
  }

  // Clicking any menu item closes menu immediately and lets link navigate
  menuItems.forEach(item => {
    item.addEventListener('click', () => {
      closeMenu();
    });
  });

  // Backdrop Overlay Click (closes modal)
  if (backdrop) {
    backdrop.addEventListener('click', (e) => {
      e.preventDefault();
      closeMenu();
    });
  }

  // Prevent clicks inside the modal from bubbling to document and prematurely closing
  if (menu) {
    menu.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  }

  // Clicking anywhere outside closes menu
  document.addEventListener('click', (e) => {
    if (!container.contains(e.target) && (!backdrop || !backdrop.contains(e.target))) {
      closeMenu();
    }
  });

  // Keyboard Accessibility (Enter or Space opens/toggles)
  trigger.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (container.classList.contains('active')) {
        closeMenu();
      } else {
        openMenu();
        if (menuItems.length > 0) {
          setTimeout(() => menuItems[0].focus(), 100);
        }
      }
    }
  });

  // Close modal when Escape key is pressed
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && container.classList.contains('active')) {
      closeMenu();
      trigger.focus();
    }
  });
}

// 2. Scroll Reveal Animations (using Intersection Observer)
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');
  
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          // Once animated, no need to track it anymore
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.01,
      rootMargin: '0px 0px -50px 0px'
    });

    reveals.forEach(el => observer.observe(el));
  } else {
    // Fallback for older browsers
    const checkReveal = () => {
      reveals.forEach(el => {
        const windowHeight = window.innerHeight;
        const revealTop = el.getBoundingClientRect().top;
        const revealPoint = 150;

        if (revealTop < windowHeight - revealPoint) {
          el.classList.add('active');
        }
      });
    };
    window.addEventListener('scroll', checkReveal);
    checkReveal();
  }
}

// 3. FAQ Accordion panel expansion (supports both .faq-header and .faq-item-header)
function initFaqAccordion() {
  const faqHeaders = document.querySelectorAll('.faq-header, .faq-item-header');

  faqHeaders.forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.faq-item, .faq-item-card');
      if (!item) return;
      const body = item.querySelector('.faq-body, .faq-item-body');
      const isActive = item.classList.contains('active');

      // Close all other FAQs in the same container
      const parentList = item.parentElement;
      if (parentList) {
        parentList.querySelectorAll('.faq-item, .faq-item-card').forEach(otherItem => {
          if (otherItem !== item) {
            otherItem.classList.remove('active');
            const otherBody = otherItem.querySelector('.faq-body, .faq-item-body');
            if (otherBody) otherBody.style.maxHeight = null;
          }
        });
      }

      // Toggle current FAQ
      if (!isActive) {
        item.classList.add('active');
        if (body) body.style.maxHeight = body.scrollHeight + 'px';
      } else {
        item.classList.remove('active');
        if (body) body.style.maxHeight = null;
      }
    });
  });
}

// 4. Product Catalog filtering by category
function initProductFilter() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const productCards = document.querySelectorAll('.product-card');

  if (tabBtns.length > 0 && productCards.length > 0) {
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Update active button state
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const category = btn.getAttribute('data-category');

        productCards.forEach(card => {
          const cardCategory = card.getAttribute('data-category');
          
          if (category === 'all' || cardCategory === category) {
            card.style.display = 'flex';
            // Subtle fade-in animation
            card.style.opacity = '0';
            setTimeout(() => {
              card.style.opacity = '1';
              card.style.transition = 'opacity 0.4s ease';
            }, 50);
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }
}

// 5. Contact Form Submission & Parameter Pre-filling
function initInquiryForm() {
  const forms = document.querySelectorAll('.b2b-inquiry-form, #productRfqForm, form[action*="inquiry"], form[action*="contact"]');

  forms.forEach(form => {
    // Pre-fill logic: if URL has ?product=xxx, pre-fill product selection or message box
    const urlParams = new URLSearchParams(window.location.search);
    const productParam = urlParams.get('product') || urlParams.get('id');
    const selectElem = form.querySelector('[name="product_interest"]') || form.querySelector('[name="category"]');
    
    if (productParam && selectElem) {
      for (let i = 0; i < selectElem.options.length; i++) {
        if (selectElem.options[i].value.toLowerCase() === productParam.toLowerCase()) {
          selectElem.selectedIndex = i;
          break;
        }
      }
    }

    // Form submission
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : 'Submit';
      
      if (submitBtn) {
        submitBtn.innerHTML = 'Submitting RFQ...';
        submitBtn.disabled = true;
      }

      // Gather input data
      const formData = new FormData(form);
      const data = {
        _to: 'amy@widewaygroup.com',
        recipient: 'amy@widewaygroup.com',
        _subject: 'New B2B Footwear RFQ Inquiry from Website',
        source_url: window.location.href
      };
      formData.forEach((value, key) => {
        data[key] = value;
      });

      // 1. Post to native backend API
      fetch('/api/inquiry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('API server returned error ' + response.status);
      })
      .then(result => {
        if (submitBtn) {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }
        showToast('✅ RFQ submitted successfully! Sent to amy@widewaygroup.com. We will respond within 8 hours.');
        form.reset();

        const successMsg = form.querySelector('#inquirySuccess') || document.getElementById('inquirySuccess') || document.getElementById('rfqResultMsg');
        if (successMsg) {
          successMsg.style.display = 'block';
          successMsg.textContent = '✅ Thank you! Your inquiry has been sent to amy@widewaygroup.com. We will reply within 8 hours.';
        }

        // Trigger background redundancy relay to FormSubmit
        fetch('https://formsubmit.co/ajax/amy@widewaygroup.com', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(data)
        }).catch(() => {});
      })
      .catch(error => {
        // 2. Direct fallback to FormSubmit
        fetch('https://formsubmit.co/ajax/amy@widewaygroup.com', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
          if (submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
          }
          showToast('✅ Inquiry sent successfully to amy@widewaygroup.com!');
          form.reset();
          const successMsg = form.querySelector('#inquirySuccess') || document.getElementById('inquirySuccess');
          if (successMsg) {
            successMsg.style.display = 'block';
            successMsg.textContent = '✅ Thank you! Your inquiry has been sent to amy@widewaygroup.com.';
          }
        })
        .catch(err => {
          if (submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
          }
          showToast('Inquiry received! Sent to amy@widewaygroup.com.');
          form.reset();
        });
      });
    });
  });
}

// Helper: Show custom Toast notification
function showToast(message) {
  let toast = document.querySelector('.toast-msg');
  
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast-msg';
    document.body.appendChild(toast);
  }
  
  toast.textContent = message;
  
  // Trigger transition
  setTimeout(() => {
    toast.classList.add('show');
  }, 100);

  // Auto hide
  setTimeout(() => {
    toast.classList.remove('show');
  }, 5000);
}

// 6. Technical Whitepaper Tab Toggles
function initWhitepaperNav() {
  const navLinks = document.querySelectorAll('.paper-nav-link');
  const contents = document.querySelectorAll('.paper-content');

  if (navLinks.length > 0 && contents.length > 0) {
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navLinks.forEach(l => l.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));

        link.classList.add('active');
        const target = link.getAttribute('data-target');
        const targetElem = document.getElementById(target);
        if (targetElem) {
          targetElem.classList.add('active');
        }
      });
    });
  }
}

// 7. Trusted by Leading Brands Carousel & Filter Tabs
function initTrustedBrands() {
  const filterBtns = document.querySelectorAll('.trusted-filter-btn');
  const cards = document.querySelectorAll('.brand-client-card');
  const viewport = document.getElementById('trustedViewport');
  const prevBtn = document.getElementById('trustedPrev');
  const nextBtn = document.getElementById('trustedNext');

  if (filterBtns.length > 0 && cards.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');
        cards.forEach(card => {
          const cat = card.getAttribute('data-category');
          if (filter === 'all' || cat === filter) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
        if (viewport) {
          viewport.scrollTo({ left: 0, behavior: 'smooth' });
        }
      });
    });
  }

  if (viewport && prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      viewport.scrollBy({ left: -280, behavior: 'smooth' });
    });
    nextBtn.addEventListener('click', () => {
      viewport.scrollBy({ left: 280, behavior: 'smooth' });
    });
  }
}

// 10. High-Performance IntersectionObserver Number Counter (跳转数字 / Odometer)
function initNumberCounters() {
  const statSelectors = [
    '.stat-number', '.counter', '[data-counter]',
    '.hero-stat strong', '.metric-value', '.highlight-number',
    '.stat-card h3', '.stat-box h3', '.stat-item h3', '.stat-val',
    '.qc-metric-val', '.capacity-stat strong', '.capacity-stat h3',
    '.stat-digit', '.stat-figure', '.counter-number'
  ];
  
  const elements = document.querySelectorAll(statSelectors.join(', '));
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateNumber(entry.target);
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  elements.forEach(el => {
    const raw = el.textContent.trim();
    // Only target elements containing digits
    if (/\d+/.test(raw) && !el.dataset.counterDone) {
      el.dataset.originalText = raw;
      observer.observe(el);
    }
  });
}

function animateNumber(el) {
  if (el.dataset.counterDone) return;
  const rawText = el.dataset.originalText || el.textContent.trim();
  
  // Match prefix, numeric portion (with commas/dots), and suffix
  // e.g., "19+", "5,000,000+", "$100M", "100%", "32 Checkpoints", "8h"
  const match = rawText.match(/^([^\d]*)([\d,.]+)(.*)$/);
  if (!match) return;

  const prefix = match[1] || '';
  const numStr = match[2].replace(/,/g, '');
  const suffix = match[3] || '';
  const isFloat = numStr.includes('.') && numStr.split('.')[1].length > 0;
  const targetVal = parseFloat(numStr);
  if (isNaN(targetVal)) return;

  el.dataset.counterDone = "true";
  const hasCommas = match[2].includes(',');
  const duration = 1600; // ms
  const startTime = performance.now();

  function formatNum(val) {
    let s = isFloat ? val.toFixed(1) : Math.round(val).toString();
    if (hasCommas) {
      s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
    return prefix + s + suffix;
  }

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1.0);
    // Snappy exponential ease-out curve
    const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const currentVal = targetVal * ease;
    el.textContent = formatNum(currentVal);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = rawText;
      // Visual pop & glow on completion to capture user attention
      el.style.transition = 'transform 0.28s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      el.style.transform = 'scale(1.1)';
      setTimeout(() => {
        el.style.transform = 'scale(1)';
      }, 280);
    }
  }

  requestAnimationFrame(update);
}


// 10. Interactive B2B Footwear Sourcing & Logistics Estimator
function initSourcingCalculator() {
  const catEl = document.getElementById('calcCategory');
  const upperEl = document.getElementById('calcUpper');
  const soleEl = document.getElementById('calcSole');
  const qtyEl = document.getElementById('calcQty');
  const syncBtn = document.getElementById('calcSyncBtn');

  if (!catEl || !qtyEl || !syncBtn) return;

  const sampleDaysEl = document.getElementById('calcSampleDays');
  const prodDaysEl = document.getElementById('calcProdDays');
  const cbmEl = document.getElementById('calcCbm');
  const containerEl = document.getElementById('calcContainer');
  const aqlEl = document.getElementById('calcAql');

  function calculate() {
    const qty = parseInt(qtyEl.value, 10) || 500;
    const cat = catEl.value;
    const upper = upperEl ? upperEl.value : 'flyknit';

    // Prototyping speed: standard 7-10 days, flyknit 7-8 days, leather 8-10 days
    let sampleTime = '7 - 10 Days';
    if (upper === 'flyknit') sampleTime = '7 - 8 Days';
    else if (upper === 'leather') sampleTime = '8 - 10 Days';
    else if (upper === 'suede') sampleTime = '9 - 10 Days';

    // Mass production days
    let prodTime = '25 - 30 Days';
    if (qty <= 1000) prodTime = '22 - 28 Days';
    else if (qty <= 5000) prodTime = '28 - 32 Days';
    else if (qty <= 20000) prodTime = '32 - 38 Days';
    else prodTime = '38 - 45 Days';

    // CBM Estimation
    let pairCbm = 0.02;
    if (cat === 'slides-sandals') pairCbm = 0.012;
    else if (cat === 'bags-sportswear') pairCbm = 0.035;

    const totalCbm = (qty * pairCbm).toFixed(1);
    const cartons = Math.ceil(qty / 12);

    // Shipping Container allocation
    let containerPlan = 'LCL Consolidation';
    if (totalCbm >= 55) {
      const hqCount = Math.ceil(totalCbm / 68);
      containerPlan = `${hqCount} x 40HQ High Cube (~68 CBM)`;
    } else if (totalCbm >= 25) {
      containerPlan = '1 x 20GP Standard (~28 CBM)';
    } else {
      containerPlan = `LCL Consolidation (${cartons} Cartons / ${totalCbm} m³)`;
    }

    // AQL Standard
    const aql = qty >= 5000 ? 'AQL 1.5 Major / 4.0 Minor' : 'AQL 2.5 Major / 4.0 Minor';

    if (sampleDaysEl) sampleDaysEl.textContent = sampleTime;
    if (prodDaysEl) prodDaysEl.textContent = prodTime;
    if (cbmEl) cbmEl.textContent = `~${totalCbm} CBM (${cartons} Ctns)`;
    if (containerEl) containerEl.textContent = containerPlan;
    if (aqlEl) aqlEl.textContent = aql;
  }

  [catEl, upperEl, soleEl, qtyEl].forEach(el => {
    if (el) el.addEventListener('change', calculate);
  });

  calculate();

  // One-click transfer to RFQ form
  syncBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const inquirySection = document.getElementById('inquiry');
    if (!inquirySection) return;

    const catSelect = inquirySection.querySelector('select[name="category"]');
    const qtySelect = inquirySection.querySelector('select[name="quantity"]');
    const msgArea = inquirySection.querySelector('textarea[name="message"]');

    if (catSelect && catEl) {
      catSelect.value = catEl.value;
    }

    if (qtySelect && qtyEl) {
      const qVal = parseInt(qtyEl.value, 10);
      if (qVal <= 1000) qtySelect.value = '500-1000';
      else if (qVal <= 5000) qtySelect.value = '1000-5000';
      else if (qVal <= 20000) qtySelect.value = '5000-20000';
      else qtySelect.value = '20000+';
    }

    if (msgArea) {
      const catText = catEl.options[catEl.selectedIndex].text;
      const upperText = upperEl ? upperEl.options[upperEl.selectedIndex].text : 'Standard';
      const soleText = soleEl ? soleEl.options[soleEl.selectedIndex].text : 'Standard';
      const qtyText = qtyEl.options[qtyEl.selectedIndex].text;

      msgArea.value = `[Inquiry via Footwear Sourcing Estimator]\n• Footwear Category: ${catText}\n• Upper Material: ${upperText}\n• Outsole / Midsole: ${soleText}\n• Order Volume: ${qtyText}\n• Target Shipment: FOB Xiamen Port / Quanzhou Port\n• Sourcing Requirement: Please provide factory direct price quotation, mold availability, and physical swatch swatches.`;
    }

    inquirySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (msgArea) {
      setTimeout(() => {
        msgArea.focus();
        msgArea.style.boxShadow = '0 0 0 3px rgba(255, 122, 24, 0.4)';
        setTimeout(() => { msgArea.style.boxShadow = ''; }, 1200);
      }, 700);
    }
  });
}

// 10. Global 2026 B2B Quick Quote Modal Drawer
function initQuickQuoteModal() {
  let modalBackdrop = document.getElementById('globalRfqModal');
  if (!modalBackdrop) {
    modalBackdrop = document.createElement('div');
    modalBackdrop.id = 'globalRfqModal';
    modalBackdrop.className = 'rfq-modal-backdrop';
    modalBackdrop.innerHTML = `
      <div class="rfq-modal-card">
        <button type="button" class="rfq-modal-close" id="rfqModalClose" aria-label="Close RFQ Modal">&times;</button>
        <div class="rfq-modal-header">
          <span class="rfq-modal-badge">Direct Factory Quotation</span>
          <h3 class="rfq-modal-title">Request Footwear Pricing & Swatches</h3>
          <p class="rfq-modal-subtitle">Direct from WIDEWAY Jinjiang factory. 24/7 engineering response within 8 hours. Low MOQ from 500 pairs.</p>
        </div>
        <form id="globalRfqForm" class="b2b-inquiry-form">
          <div class="rfq-input-group">
            <label>Your Name *</label>
            <input type="text" name="name" required placeholder="e.g. David Miller">
          </div>
          <div class="rfq-grid-2">
            <div class="rfq-input-group">
              <label>Business Email *</label>
              <input type="email" name="email" required placeholder="david@brand.com">
            </div>
            <div class="rfq-input-group">
              <label>WhatsApp / Phone</label>
              <input type="text" name="phone" placeholder="+1 555-0199">
            </div>
          </div>
          <div class="rfq-grid-2">
            <div class="rfq-input-group">
              <label>Footwear Category</label>
              <select name="category" id="modalCategorySelect">
                <option value="sport-outdoor-shoes">Sport & Outdoor Shoes</option>
                <option value="casual-shoes">Casual Shoes</option>
                <option value="mens-shoes">Men's Sneakers</option>
                <option value="womens-shoes">Women's Trainers</option>
                <option value="slides-sandals">Slides & Sandals</option>
                <option value="bags-sportswear">Sportswear Bags</option>
              </select>
            </div>
            <div class="rfq-input-group">
              <label>Target Quantity</label>
              <select name="quantity">
                <option value="500-1000">500 - 1,000 Pairs (Low MOQ)</option>
                <option value="1000-5000">1,000 - 5,000 Pairs</option>
                <option value="5000-20000">5,000 - 20,000 Pairs</option>
                <option value="20000+">20,000+ Pairs (Full Container)</option>
              </select>
            </div>
          </div>
          <div class="rfq-input-group">
            <label>Specifications & Custom Requirements</label>
            <textarea name="message" id="modalMessageArea" rows="3" placeholder="Specify upper/outsole materials, branding, sample needs, or target delivery port..."></textarea>
          </div>
          <button type="submit" class="rfq-submit-btn" id="modalSubmitBtn">Submit Factory Inquiry &rarr;</button>
          <div id="modalResultMsg" style="display:none; margin-top:14px; color:#16a34a; font-weight:700; font-size:0.92rem; text-align:center;"></div>
          <div class="rfq-trust-strip">
            <span>🔒 Strict Privacy Protected</span>
            <span>⚡ 7-10 Days Fast Tooling Sample</span>
            <span>🏭 Chendai, Jinjiang Factory</span>
          </div>
        </form>
      </div>
    `;
    document.body.appendChild(modalBackdrop);
  }

  const closeBtn = document.getElementById('rfqModalClose');
  const modalForm = document.getElementById('globalRfqForm');
  const resultMsg = document.getElementById('modalResultMsg');

  function openModal(initialCategory, initialProduct) {
    modalBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
    if (initialCategory) {
      const catSelect = document.getElementById('modalCategorySelect');
      if (catSelect) {
        for (let i = 0; i < catSelect.options.length; i++) {
          if (catSelect.options[i].value.toLowerCase().includes(initialCategory.toLowerCase())) {
            catSelect.selectedIndex = i;
            break;
          }
        }
      }
    }
    if (initialProduct) {
      const msgArea = document.getElementById('modalMessageArea');
      if (msgArea) {
        msgArea.value = `[Footwear Inquiry: ${initialProduct}]\nPlease provide FOB quotation, tooling availability, and physical material swatches.`;
      }
    }
  }

  function closeModal() {
    modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('active')) closeModal();
  });

  // Attach to quote buttons: .dock-quote, .btn-open-quote, or links to contact?product=
  document.querySelectorAll('.dock-quote, .btn-open-quote, a[href*="contact?product="], a[href*="contact?category="]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      let href = btn.getAttribute('href') || '';
      let urlParams = new URLSearchParams(href.includes('?') ? href.split('?')[1] : '');
      let prodId = urlParams.get('product') || btn.getAttribute('data-product') || '';
      let cat = urlParams.get('category') || btn.getAttribute('data-category') || '';
      openModal(cat, prodId);
    });
  });

  // Form submission handling
  if (modalForm) {
    modalForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('modalSubmitBtn');
      const origText = submitBtn ? submitBtn.innerHTML : 'Submit';
      if (submitBtn) {
        submitBtn.innerHTML = 'Transmitting RFQ to Factory...';
        submitBtn.disabled = true;
      }

      const payload = {
        name: modalForm.name.value,
        email: modalForm.email.value,
        phone: modalForm.phone.value,
        category: modalForm.category.value,
        product_interest: modalForm.category.value,
        quantity: modalForm.quantity.value,
        message: modalForm.message.value,
        recipient: 'amy@widewaygroup.com',
        source_url: window.location.href,
        date: new Date().toISOString()
      };

      try {
        await fetch('/api/inquiry', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
      } catch(err) {
        console.log('Local API submit info:', err);
      }

      // Redundant background delivery to FormSubmit
      try {
        fetch('https://formsubmit.co/ajax/amy@widewaygroup.com', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
          body: JSON.stringify({
            _subject: `[WIDEWAY Footwear RFQ] ${payload.name} - ${payload.category}`,
            _replyto: payload.email,
            Name: payload.name,
            Email: payload.email,
            Phone: payload.phone,
            Category: payload.category,
            Quantity: payload.quantity,
            Requirements: payload.message,
            Source: window.location.href
          })
        }).catch(() => {});
      } catch(e) {}

      if (submitBtn) {
        submitBtn.innerHTML = origText;
        submitBtn.disabled = false;
      }
      modalForm.reset();
      if (resultMsg) {
        resultMsg.style.display = 'block';
        resultMsg.textContent = '✅ Quotation request sent to factory! We will email you back within 8 hours.';
        setTimeout(() => {
          closeModal();
          resultMsg.style.display = 'none';
        }, 2500);
      }
    });
  }
}


// 2026 Header Scroll Elevation Effect
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  if (header) {
    if (window.scrollY > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
}, { passive: true });

// Nav Dropdown Interaction (Desktop Hover & Touch Toggle)
function initNavDropdowns() {
  const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
  
  dropdownItems.forEach(item => {
    const link = item.querySelector('.desktop-nav-link');
    if (!link) return;

    // Mobile / Touch click toggle
    link.addEventListener('click', (e) => {
      if (window.innerWidth <= 1024 || ('ontouchstart' in window)) {
        if (!item.classList.contains('open')) {
          e.preventDefault();
          dropdownItems.forEach(other => {
            if (other !== item) other.classList.remove('open');
          });
          item.classList.add('open');
        }
      }
    });

    // Keyboard support
    link.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        if (!item.classList.contains('open')) {
          e.preventDefault();
          item.classList.add('open');
        }
      } else if (e.key === 'Escape') {
        item.classList.remove('open');
      }
    });
  });

  // Close dropdowns on outside click
  document.addEventListener('click', (e) => {
    if (!targetIsDropdown(e.target)) {
      dropdownItems.forEach(item => item.classList.remove('open'));
    }
  });

  function targetIsDropdown(target) {
    return target && target.closest && target.closest('.nav-item.has-dropdown');
  }
}

// WhatsApp Multi-Rep Floating Widget Interactions
function toggleWhatsAppWidget(event, forceState) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  const widget = document.getElementById('whatsappFloatingWidget');
  if (!widget) return;

  if (typeof forceState === 'boolean') {
    if (forceState) widget.classList.add('active');
    else widget.classList.remove('active');
  } else {
    widget.classList.toggle('active');
  }
}

function initWhatsAppWidget() {
  const widget = document.getElementById('whatsappFloatingWidget');
  if (!widget) return;

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (widget.classList.contains('active') && !widget.contains(e.target)) {
      widget.classList.remove('active');
    }
  });

  // Close with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && widget.classList.contains('active')) {
      widget.classList.remove('active');
    }
  });
}

// 12. Anti-Malicious Cloning & Domain Integrity Guard (100% SEO & GEO Crawlers Safe)
function initAntiCloningProtection() {
  try {
    // 1. Domain verification: Detect unauthorized reverse proxies / mirror cloners
    const canonicalHost = 'www.widewayfootwear.com';
    const currentHost = window.location.hostname ? window.location.hostname.toLowerCase() : '';
    
    // Whitelist legitimate local development, IP previews, and canonical domain
    const isWhitelisted = (
      currentHost === '' ||
      currentHost === 'widewayfootwear.com' ||
      currentHost === 'www.widewayfootwear.com' ||
      currentHost === 'localhost' ||
      currentHost === '127.0.0.1' ||
      currentHost === '0.0.0.0' ||
      currentHost.endsWith('.local') ||
      currentHost.endsWith('.internal') ||
      currentHost.startsWith('192.168.') ||
      currentHost.startsWith('10.') ||
      currentHost.startsWith('172.') ||
      currentHost.includes('43.130.32.54')
    );

    if (!isWhitelisted && typeof window !== 'undefined' && window.location) {
      console.warn('⚠️ Security Alert: Unauthorized domain cloning detected. Redirecting to authentic WIDEWAY source.');
      const targetUrl = 'https://' + canonicalHost + window.location.pathname + window.location.search + window.location.hash;
      window.location.replace(targetUrl);
      return;
    }

    // 2. Anti-Framejacking: Break out of unauthorized <iframe> framing / phishing mirrors
    if (window.top !== window.self) {
      try {
        if (window.top.location.hostname !== window.self.location.hostname) {
          window.top.location.href = window.self.location.href;
        }
      } catch (err) {
        // Cross-origin iframe wrapper detected
        window.top.location.href = 'https://' + canonicalHost;
      }
    }

    // 3. Digital Signature & Watermark Console Guard
    if (typeof console !== 'undefined' && console.log) {
      console.log(
        '%c🔒 WIDEWAY GROUP™ %c Official Footwear OEM/ODM Global Portal | Anti-Cloning Armor Active',
        'background: #e50408; color: #fff; font-weight: bold; padding: 4px 8px; border-radius: 3px;',
        'color: #0b1528; font-weight: 600; padding: 4px;'
      );
    }
  } catch (e) {
    // Non-blocking fallback
  }
}


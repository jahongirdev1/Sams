// Mobile menu functionality
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('active');
}

// Hero slider functionality
let currentSlide = 0;
let slides = [];
let totalSlides = 0;

function showSlide(index) {
    if (!slides.length) {
        return;
    }

    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });

    // Update dots
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

function nextSlide() {
    if (totalSlides <= 1) {
        return;
    }

    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    if (totalSlides <= 1) {
        return;
    }

    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

function goToSlide(index) {
    if (index < 0 || index >= totalSlides) {
        return;
    }

    currentSlide = index;
    showSlide(currentSlide);
}

// Initialize slider
document.addEventListener('DOMContentLoaded', function() {
    const heroSlider = document.getElementById('heroSlider');
    slides = heroSlider ? heroSlider.querySelectorAll('.slide') : [];
    totalSlides = slides.length;

    if (!totalSlides) {
        return;
    }

    if (heroSlider) {
        heroSlider.classList.add('is-ready');
    }

    // Create dots for slider
    const sliderDots = document.getElementById('sliderDots');
    if (sliderDots) {
        sliderDots.innerHTML = '';
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('div');
            dot.className = 'dot';
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            sliderDots.appendChild(dot);
        }
    }

    // Show the first slide immediately
    currentSlide = 0;
    showSlide(currentSlide);

    // Auto-play slider
    if (totalSlides > 1) {
        setInterval(nextSlide, 5000);
    }

    // Phone mask
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('7')) {
                value = value.substring(1);
            }
            if (value.length > 0) {
                if (value.length <= 3) {
                    value = `+7 (${value}`;
                } else if (value.length <= 6) {
                    value = `+7 (${value.slice(0, 3)}) ${value.slice(3)}`;
                } else if (value.length <= 8) {
                    value = `+7 (${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
                } else {
                    value = `+7 (${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 8)}-${value.slice(8, 10)}`;
                }
            }
            e.target.value = value;
        });
    }
});

function makeHorizontalScroll(el) {
    if (!el) return;
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;

    // Drag to scroll (мышью)
    el.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - el.offsetLeft;
        scrollLeft = el.scrollLeft;
        el.classList.add('dragging');
    });
    window.addEventListener('mouseup', () => {
        isDown = false;
        el.classList.remove('dragging');
    });
    el.addEventListener('mouseleave', () => {
        isDown = false;
        el.classList.remove('dragging');
    });
    el.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - el.offsetLeft;
        const walk = (x - startX);
        el.scrollLeft = scrollLeft - walk;
    });

    // Вертикальное колесо → горизонтальный скролл
    el.addEventListener('wheel', (e) => {
        // если пользователь крутит вертикально — скроллим вбок
        if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
            el.scrollLeft += e.deltaY;
            e.preventDefault();
        }
    }, { passive: false });
}

document.addEventListener('DOMContentLoaded', function () {
    const scroller = document.getElementById('catScroller') || document.getElementById('catRow');
    makeHorizontalScroll(scroller);
});

// Contact form functionality
function submitForm(event) {
    event.preventDefault();
    
    const form = document.getElementById('contactForm');
    const formSuccess = document.getElementById('formSuccess');
    
    // Simple validation
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const message = document.getElementById('message').value.trim();
    
    if (!name || !phone || !message) {
        alert('Пожалуйста, заполните все обязательные поля.');
        return false;
    }
    
    // Simulate form submission
    form.style.display = 'none';
    formSuccess.style.display = 'block';
    
    // Reset form after 5 seconds (in real implementation, this would be handled by server)
    setTimeout(() => {
        form.reset();
        form.style.display = 'block';
        formSuccess.style.display = 'none';
    }, 5000);
    
    return false;
}

// Product detail gallery functionality
function changeMainImage(src) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = src;
    }
    
    // Update active thumbnail
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        thumb.classList.toggle('active', thumb.src === src);
    });
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Video placeholder click functionality
document.addEventListener('DOMContentLoaded', function() {
    const videoPlaceholders = document.querySelectorAll('.video-placeholder');
    
    videoPlaceholders.forEach(placeholder => {
        placeholder.addEventListener('click', function() {
            // In a real implementation, this would open a video modal or redirect to video
            alert('Здесь будет воспроизведено видео о компании');
        });
    });
});

// Intersection Observer for animations
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.product-card, .stat-card, .mission-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

(function () {
  function initCatalogFilter() {
    const scroller = document.getElementById("catRow") || document.getElementById("catScroller");
    const grid = document.getElementById("productsGrid");
    if (!grid) return;

    // делегирование кликов
    document.addEventListener("click", async (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;

      const slug = btn.dataset.cat || (btn.dataset.all ? "all" : null);
      if (!slug) return;

      e.preventDefault();

      // активная кнопка
      document.querySelectorAll(".filter-btn.active").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Плавное обновление грида
      grid.style.opacity = "0.5";

      const params = new URLSearchParams(window.location.search);
      params.set("category", slug);
      params.delete("page");
      params.set("partial", "1");

      try {
        const resp = await fetch(`${window.location.pathname}?${params.toString()}`, {
          headers: {"X-Requested-With": "fetch"}
        });
        const html = await resp.text();
        grid.innerHTML = html;
        grid.style.opacity = "1";

        // обновляем URL (без перезагрузки)
        params.delete("partial");
        const baseSearch = params.toString();
        const url = baseSearch ? `${window.location.pathname}?${baseSearch}#grid` : `${window.location.pathname}#grid`;
        window.history.pushState({cat: slug}, "", url);

        // оставаться на месте: скролл к гриду (на всякий случай)
        document.getElementById("grid")?.scrollIntoView({block: "start", behavior: "smooth"});
      } catch (err) {
        // фоллбек: обычная навигация с якорем
        params.delete("partial");
        const fallbackSearch = params.toString();
        const fallbackUrl = fallbackSearch ? `${window.location.pathname}?${fallbackSearch}#grid` : `${window.location.pathname}#grid`;
        window.location.href = fallbackUrl;
      }
    });

    // если пришли по ссылке/Back — не прыгать наверх
    window.addEventListener("popstate", () => {
      const params = new URLSearchParams(location.search);
      const slug = params.get("category") || "all";
      // подсветим кнопку
      document.querySelectorAll(".filter-btn.active").forEach(b => b.classList.remove("active"));
      const activeBtn = document.querySelector(`.filter-btn[data-cat="${slug}"], .filter-btn[data-all="${slug==='all'?'1':''}"]`);
      activeBtn?.classList.add("active");
      // при навигации браузера можно подгрузить частично
      const fetchParams = new URLSearchParams(params.toString());
      fetchParams.set("category", slug);
      fetchParams.delete("page");
      fetchParams.set("partial", "1");
      fetch(`${window.location.pathname}?${fetchParams.toString()}`)
        .then(r => r.text())
        .then(html => { grid.innerHTML = html; });
    });

    // если мы зашли с #grid — прокрутим к нему
    if (location.hash === "#grid") {
      document.getElementById("grid")?.scrollIntoView({block: "start"});
    }
  }

  document.addEventListener("DOMContentLoaded", initCatalogFilter);
})();

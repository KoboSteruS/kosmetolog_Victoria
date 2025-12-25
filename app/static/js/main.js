/**
 * Основной JavaScript файл для лендинга клиники "Виктория"
 * Обработка форм, модальных окон, анимаций и интерактивности
 */

// === ГЛОБАЛЬНЫЕ ФУНКЦИИ (должны быть доступны сразу для onclick) ===

/**
 * Модальное окно всех отзывов
 */
window.openAllReviewsModal = function() {
    console.log('🔍 Открываем модальное окно отзывов...');
    const modal = document.getElementById('allReviewsModal');
    console.log('Modal element:', modal);
    
    if (modal) {
        console.log('✅ Modal найден, открываем...');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Загружаем все отзывы
        loadAllReviews();
    } else {
        console.error('❌ Modal не найден! ID: allReviewsModal');
    }
};

window.closeAllReviewsModal = function() {
    const modal = document.getElementById('allReviewsModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
};

/**
 * Загрузка всех отзывов
 */
function loadAllReviews() {
    const container = document.getElementById('allReviewsList');
    
    fetch('/api/reviews')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.length > 0) {
                container.innerHTML = data.data.map(review => `
                    <div class="review-card" style="margin-bottom: 20px;">
                        <div class="review-header">
                            <div class="review-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                            <div class="review-author">
                                <h4 class="review-name">${escapeHtml(review.name)}</h4>
                                <div class="review-rating">
                                    ${'<i class="fas fa-star"></i>'.repeat(review.rating)}
                                    ${'<i class="far fa-star"></i>'.repeat(5 - review.rating)}
                                </div>
                            </div>
                        </div>
                        <p class="review-text">${escapeHtml(review.text)}</p>
                        <div class="review-date">
                            ${formatReviewDate(review.created_at)}
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = `
                    <div class="no-reviews">
                        <i class="fas fa-comments"></i>
                        <p>Отзывов пока нет</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки отзывов:', error);
            container.innerHTML = `
                <div class="no-reviews">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Ошибка загрузки отзывов</p>
                </div>
            `;
        });
}

/**
 * Экранирование HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Форматирование даты отзыва
 */
function formatReviewDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// === ИНИЦИАЛИЗАЦИЯ ===
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Инициализация приложения...');
    initAOS();
    initSmoothScroll();
    initMobileMenu();
    initServiceFilters();
    initForms();
    initRatingInput();
    initHeaderScroll();
    initCounters();
    initFAQ();
    initFloatingCTA();
    initBeforeAfter();
    
    console.log('✅ Все функции загружены');
    console.log('Доступные модальные функции:', {
        openAllReviewsModal: typeof window.openAllReviewsModal,
        closeAllReviewsModal: typeof window.closeAllReviewsModal
    });
});

/**
 * Инициализация библиотеки AOS для анимаций при скролле
 * Оптимизировано для производительности
 */
function initAOS() {
    if (typeof AOS !== 'undefined') {
        // Отключаем AOS на слабых устройствах для экономии ресурсов
        const isLowPerformance = window.matchMedia('(max-width: 768px)').matches || 
                                 navigator.hardwareConcurrency < 4;
        
        AOS.init({
            duration: isLowPerformance ? 300 : 400, // Еще быстрее на мобильных
            easing: 'ease-out',
            once: true, // Анимация только один раз
            offset: 50,
            disable: isLowPerformance ? 'mobile' : false, // Отключаем на мобильных если совсем слабое устройство
            throttleDelay: 99, // Задержка между обновлениями (оптимизация производительности)
            debounceDelay: 50 // Задержка при resize (оптимизация)
        });
    }
}

/**
 * Плавная прокрутка к якорным ссылкам
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Игнорируем пустые якоря
            if (href === '#' || href === '#!') {
                return;
            }
            
            e.preventDefault();
            
            const target = document.querySelector(href);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Мобильное меню (гамбургер)
 */
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
        
        // Закрытие меню при клике на ссылку
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
}

/**
 * Изменение хедера при скролле
 */
function initHeaderScroll() {
    const header = document.getElementById('header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/**
 * Фильтрация услуг по категориям
 */
function initServiceFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const serviceCards = document.querySelectorAll('.service-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Обновляем активную кнопку
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Фильтруем карточки
            serviceCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                    // Добавляем анимацию появления
                    card.style.animation = 'fadeIn 0.5s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Инициализация input для рейтинга
 */
function initRatingInput() {
    const ratingInput = document.getElementById('ratingInput');
    const ratingField = document.getElementById('rating');
    
    if (ratingInput && ratingField) {
        const stars = ratingInput.querySelectorAll('i');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = this.getAttribute('data-rating');
                ratingField.value = rating;
                
                // Обновляем визуализацию
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.remove('far');
                        s.classList.add('fas', 'active');
                    } else {
                        s.classList.remove('fas', 'active');
                        s.classList.add('far');
                    }
                });
            });
            
            // Эффект при наведении
            star.addEventListener('mouseenter', function() {
                const rating = this.getAttribute('data-rating');
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('active');
                    }
                });
            });
        });
        
        // Убираем эффект при уходе мыши
        ratingInput.addEventListener('mouseleave', function() {
            const currentRating = ratingField.value;
            stars.forEach((s, i) => {
                if (i >= currentRating) {
                    s.classList.remove('active');
                }
            });
        });
    }
}

/**
 * Инициализация всех форм
 */
function initForms() {
    // Форма записи в модальном окне
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', handleAppointmentSubmit);
    }
    
    // Форма записи в контактах
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleAppointmentSubmit);
    }
    
    // Форма отзыва
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', handleReviewSubmit);
    }
    
    // Маска для телефона
    initPhoneMask();
}

/**
 * Маска для поля телефона
 */
function initPhoneMask() {
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 0) {
                if (value[0] === '8') {
                    value = '7' + value.slice(1);
                }
                
                let formatted = '+7';
                
                if (value.length > 1) {
                    formatted += ' (' + value.substring(1, 4);
                }
                if (value.length >= 5) {
                    formatted += ') ' + value.substring(4, 7);
                }
                if (value.length >= 8) {
                    formatted += '-' + value.substring(7, 9);
                }
                if (value.length >= 10) {
                    formatted += '-' + value.substring(9, 11);
                }
                
                e.target.value = formatted;
            }
        });
    });
}

/**
 * Обработка отправки формы записи
 */
async function handleAppointmentSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const messageEl = form.querySelector('.form-message');
    
    // Получаем данные формы
    const formData = {
        name: form.querySelector('[name="name"]').value,
        phone: form.querySelector('[name="phone"]').value,
        service: form.querySelector('[name="service"]')?.value || '',
        comment: form.querySelector('[name="comment"]')?.value || '',
        agreed_to_processing: form.querySelector('[name="agreed_to_processing"]').checked,
        agreed_to_newsletter: form.querySelector('[name="agreed_to_newsletter"]')?.checked || false
    };
    
    // Валидация
    if (!formData.name || !formData.phone) {
        showFormMessage(messageEl, 'error', 'Заполните все обязательные поля');
        return;
    }
    
    if (!formData.agreed_to_processing) {
        showFormMessage(messageEl, 'error', 'Необходимо согласие на обработку персональных данных');
        return;
    }
    
    // Показываем загрузку
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    hideFormMessage(messageEl);
    
    try {
        const response = await fetch('/api/appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showFormMessage(messageEl, 'success', data.message);
            form.reset();
            
            // Закрываем модальное окно через 2 секунды
            setTimeout(() => {
                closeAppointmentModal();
            }, 2000);
        } else {
            let errorMessage = data.message || 'Произошла ошибка при отправке заявки';
            
            // Обработка ошибок валидации
            if (data.errors && Array.isArray(data.errors)) {
                errorMessage = data.errors.map(err => err.msg).join(', ');
            }
            
            showFormMessage(messageEl, 'error', errorMessage);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showFormMessage(messageEl, 'error', 'Ошибка при отправке данных. Попробуйте позже.');
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Обработка отправки формы отзыва
 */
async function handleReviewSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const messageEl = form.querySelector('.form-message');
    
    // Получаем данные формы
    const formData = {
        name: form.querySelector('[name="name"]').value,
        rating: parseInt(form.querySelector('[name="rating"]').value),
        text: form.querySelector('[name="text"]').value
    };
    
    // Валидация
    if (!formData.name || !formData.rating || !formData.text) {
        showFormMessage(messageEl, 'error', 'Заполните все поля');
        return;
    }
    
    if (formData.rating < 1 || formData.rating > 5) {
        showFormMessage(messageEl, 'error', 'Выберите оценку от 1 до 5');
        return;
    }
    
    // Показываем загрузку
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    hideFormMessage(messageEl);
    
    try {
        const response = await fetch('/api/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showFormMessage(messageEl, 'success', data.message);
            form.reset();
            
            // Сбрасываем рейтинг
            const stars = document.querySelectorAll('#ratingInput i');
            stars.forEach(star => {
                star.classList.remove('fas', 'active');
                star.classList.add('far');
            });
            
            // Закрываем модальное окно через 2 секунды
            setTimeout(() => {
                closeReviewModal();
            }, 2000);
        } else {
            let errorMessage = data.message || 'Произошла ошибка при отправке отзыва';
            
            if (data.errors && Array.isArray(data.errors)) {
                errorMessage = data.errors.map(err => err.msg).join(', ');
            }
            
            showFormMessage(messageEl, 'error', errorMessage);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showFormMessage(messageEl, 'error', 'Ошибка при отправке данных. Попробуйте позже.');
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Показать сообщение формы
 */
function showFormMessage(element, type, message) {
    if (!element) return;
    
    element.className = `form-message ${type}`;
    element.textContent = message;
    element.style.display = 'block';
}

/**
 * Скрыть сообщение формы
 */
function hideFormMessage(element) {
    if (!element) return;
    
    element.style.display = 'none';
}

/**
 * Открыть модальное окно записи
 */
function openAppointmentModal(serviceName = '', specialistName = '') {
    const modal = document.getElementById('appointmentModal');
    if (!modal) return;
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Предзаполняем услугу если передана
    if (serviceName) {
        const serviceSelect = modal.querySelector('[name="service"]');
        if (serviceSelect) {
            // Пытаемся найти опцию с таким названием
            const option = Array.from(serviceSelect.options).find(
                opt => opt.value === serviceName
            );
            if (option) {
                serviceSelect.value = serviceName;
            } else {
                // Если не нашли, добавляем новую опцию
                const newOption = document.createElement('option');
                newOption.value = serviceName;
                newOption.textContent = serviceName;
                newOption.selected = true;
                serviceSelect.appendChild(newOption);
            }
        }
    }
    
    // Добавляем имя специалиста в комментарий если передано
    if (specialistName) {
        const commentField = modal.querySelector('[name="comment"]');
        if (commentField) {
            commentField.value = `Хочу записаться к ${specialistName}`;
        }
    }
}

/**
 * Закрыть модальное окно записи
 */
function closeAppointmentModal() {
    const modal = document.getElementById('appointmentModal');
    if (!modal) return;
    
    modal.classList.remove('active');
    document.body.style.overflow = '';
    
    // Очищаем форму и сообщения
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
        const messageEl = form.querySelector('.form-message');
        hideFormMessage(messageEl);
    }
}

/**
 * Открыть модальное окно отзыва
 */
function openReviewModal() {
    const modal = document.getElementById('reviewModal');
    if (!modal) return;
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Закрыть модальное окно отзыва
 */
function closeReviewModal() {
    const modal = document.getElementById('reviewModal');
    if (!modal) return;
    
    modal.classList.remove('active');
    document.body.style.overflow = '';
    
    // Очищаем форму и сообщения
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
        const messageEl = form.querySelector('.form-message');
        hideFormMessage(messageEl);
    }
}

/**
 * Закрытие модальных окон по клику вне контента
 */
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

/**
 * Закрытие модальных окон по Escape
 */
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
});

/**
 * Анимация появления элементов
 */
const fadeInAnimation = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;

// Добавляем анимацию в стили
const style = document.createElement('style');
style.textContent = fadeInAnimation;
document.head.appendChild(style);

/**
 * Открыть модальное окно всех услуг
 */
function openAllServicesModal() {
    const modal = document.getElementById('allServicesModal');
    if (!modal) return;
    
    // Загружаем все услуги
    loadAllServices();
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Закрыть модальное окно всех услуг
 */
function closeAllServicesModal() {
    const modal = document.getElementById('allServicesModal');
    if (!modal) return;
    
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Загрузить все услуги в модальное окно
 */
function loadAllServices() {
    const container = document.getElementById('allServicesList');
    if (!container) return;
    
    // Все услуги (те же что и на главной)
    const allServices = [
        {"name": "Прессотерапия", "price": "от 1 500 ₽", "category": "Аппаратная косметология"},
        {"name": "Пилинг срединный", "price": "от 4 700 ₽", "category": "Пилинги"},
        {"name": "Биоревитализация лица", "price": "от 7 000 ₽", "category": "Инъекционные процедуры"},
        {"name": "Мезотерапия лица", "price": "от 5 000 ₽", "category": "Инъекционные процедуры"},
        {"name": "Мезотерапия головы", "price": "от 4 800 ₽", "category": "Инъекционные процедуры"},
        {"name": "Фотолечение / фототерапия", "price": "от 3 200 ₽", "category": "Аппаратная косметология"},
        {"name": "Уходовая линия Line Repair (CHRISTINA)", "price": "от 4 900 ₽", "category": "Косметология"},
        {"name": "Чистка лица атравматическая", "price": "от 5 700 ₽", "category": "Косметология"},
        {"name": "Чистка лица комбинированная", "price": "от 3 800 ₽", "category": "Косметология"},
        {"name": "Чистка лица ультразвуковая", "price": "от 2 000 ₽", "category": "Косметология"},
        {"name": "Пилинг поверхностный", "price": "от 2 500 ₽", "category": "Пилинги"},
        {"name": "LPG-массаж", "price": "от 700 ₽", "category": "Массажи лица"},
        {"name": "Пилинг карбоновый", "price": "от 3 500 ₽", "category": "Пилинги"},
        {"name": "Ручной массаж лица", "price": "от 1 800 ₽", "category": "Массажи лица"},
        {"name": "RF-лифтинг", "price": "от 2 300 ₽", "category": "Аппаратная косметология"},
        {"name": "Пилинг алмазный", "price": "от 3 000 ₽", "category": "Пилинги"},
        {"name": "Вакуумный массаж лица", "price": "от 2 300 ₽", "category": "Массажи лица"},
        {"name": "Альгинатная маска", "price": "от 1 200 ₽", "category": "Косметология"},
        {"name": "Регенерация кожи", "price": "от 2 800 ₽", "category": "Косметология"},
        {"name": "Глубокое увлажнение", "price": "от 3 700 ₽", "category": "Косметология"},
        {"name": "Безинъекционная мезотерапия", "price": "от 2 200 ₽", "category": "Косметология"},
        {"name": "Лазерная эпиляция", "price": "от 600 ₽", "category": "Аппаратная косметология"},
        {"name": "Карбокситерапия", "price": "от 2 500 ₽", "category": "Инъекционные процедуры"},
        {"name": "Микротоковая терапия", "price": "от 2 200 ₽", "category": "Аппаратная косметология"}
    ];
    
    // Группируем по категориям
    const categories = {};
    allServices.forEach(service => {
        if (!categories[service.category]) {
            categories[service.category] = [];
        }
        categories[service.category].push(service);
    });
    
    // Генерируем HTML
    let html = '';
    for (const [category, services] of Object.entries(categories)) {
        html += `
            <div class="service-category-block" data-category="${category}">
                <h3 class="category-title">
                    <i class="fas fa-chevron-right"></i>
                    ${category}
                </h3>
                <div class="services-list">
        `;
        
        services.forEach(service => {
            html += `
                <div class="service-item">
                    <div class="service-info">
                        <span class="service-item-name">${service.name}</span>
                        <span class="service-item-price">${service.price}</span>
                    </div>
                    <button class="btn btn-sm btn-outline" onclick="closeAllServicesModal(); openAppointmentModal('${service.name}');">
                        Записаться
                    </button>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    container.innerHTML = html;
    
    // Добавляем фильтрацию в модальном окне
    initModalServicesFilter();
}

/**
 * Фильтрация услуг в модальном окне
 */
function initModalServicesFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn-modal');
    const categoryBlocks = document.querySelectorAll('.service-category-block');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Обновляем активную кнопку
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Фильтруем блоки
            categoryBlocks.forEach(block => {
                if (category === 'all' || block.getAttribute('data-category') === category) {
                    block.style.display = 'block';
                } else {
                    block.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Анимированные счётчики достижений
 */
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    let animated = false;
    
    const animateCounters = () => {
        if (animated) return;
        
        const statsSection = document.querySelector('.stats-section');
        if (!statsSection) return;
        
        const rect = statsSection.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isVisible) {
            animated = true;
            
            counters.forEach(counter => {
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000; // 2 секунды
                const increment = target / (duration / 16); // 60 FPS
                let current = 0;
                
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };
                
                updateCounter();
            });
        }
    };
    
    window.addEventListener('scroll', animateCounters);
    animateCounters(); // Проверяем сразу при загрузке
}

/**
 * FAQ аккордеон
 */
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Закрываем все открытые
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });
            
            // Открываем текущий, если он был закрыт
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

/**
 * Плавающая кнопка записи
 */
function initFloatingCTA() {
    const floatingCta = document.getElementById('floatingCta');
    if (!floatingCta) return;
    
    let lastScrollTop = 0;
    
    const handleScroll = () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const heroHeight = window.innerHeight;
        
        // Показываем кнопку после прокрутки первого экрана
        if (scrollTop > heroHeight) {
            floatingCta.classList.add('visible');
        } else {
            floatingCta.classList.remove('visible');
        }
        
        lastScrollTop = scrollTop;
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Проверяем сразу при загрузке
}

/**
 * Интерактивное сравнение До/После
 */
function initBeforeAfter() {
    const containers = document.querySelectorAll('.comparison-container');
    
    containers.forEach((container, index) => {
        // Создаём структуру для сравнения
        const beforeImg = container.querySelector('.comparison-image');
        if (!beforeImg) return;
        
        // Меняем местами: beforeImg показываем как "До" (проблемная кожа)
        // Создаём изображение "После" (чистая кожа)
        const afterImg = document.createElement('img');
        afterImg.src = beforeImg.src.replace('before', 'after');
        afterImg.alt = 'После';
        afterImg.className = 'comparison-image comparison-after';
        afterImg.style.position = 'absolute';
        afterImg.style.top = '0';
        afterImg.style.left = '0';
        afterImg.style.width = '100%';
        afterImg.style.height = '100%';
        afterImg.style.objectFit = 'cover';
        afterImg.style.clipPath = 'inset(0 0 0 50%)'; // Показываем справа
        
        container.appendChild(afterImg);
        
        // Добавляем слайдер
        const slider = document.createElement('div');
        slider.className = 'comparison-slider';
        slider.style.left = '50%';
        container.appendChild(slider);
        
        let isDragging = false;
        
        const updateSlider = (x) => {
            const rect = container.getBoundingClientRect();
            let position = ((x - rect.left) / rect.width) * 100;
            position = Math.max(0, Math.min(100, position));
            
            slider.style.left = position + '%';
            afterImg.style.clipPath = `inset(0 0 0 ${position}%)`; // После справа
        };
        
        const startDrag = (e) => {
            isDragging = true;
            container.style.cursor = 'ew-resize';
            updateSlider(e.type.includes('mouse') ? e.pageX : e.touches[0].pageX);
        };
        
        const stopDrag = () => {
            isDragging = false;
            container.style.cursor = 'default';
        };
        
        const onDrag = (e) => {
            if (!isDragging) return;
            e.preventDefault();
            updateSlider(e.type.includes('mouse') ? e.pageX : e.touches[0].pageX);
        };
        
        // События мыши
        slider.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', onDrag);
        document.addEventListener('mouseup', stopDrag);
        
        // События тач
        slider.addEventListener('touchstart', startDrag);
        document.addEventListener('touchmove', onDrag);
        document.addEventListener('touchend', stopDrag);
        
        // Клик по контейнеру
        container.addEventListener('click', (e) => {
            if (e.target !== slider) {
                updateSlider(e.pageX);
            }
        });
    });
}

// Экспортируем функции для использования из HTML
window.openAppointmentModal = openAppointmentModal;
window.closeAppointmentModal = closeAppointmentModal;
window.openReviewModal = openReviewModal;
window.closeReviewModal = closeReviewModal;
window.openAllServicesModal = openAllServicesModal;
window.closeAllServicesModal = closeAllServicesModal;
// openAllReviewsModal и closeAllReviewsModal уже экспортированы при определении


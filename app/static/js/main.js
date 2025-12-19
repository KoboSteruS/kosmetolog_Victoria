/**
 * Основной JavaScript файл для лендинга клиники "Виктория"
 * Обработка форм, модальных окон, анимаций и интерактивности
 */

// === ИНИЦИАЛИЗАЦИЯ ===
document.addEventListener('DOMContentLoaded', function() {
    initAOS();
    initSmoothScroll();
    initMobileMenu();
    initServiceFilters();
    initForms();
    initRatingInput();
    initHeaderScroll();
});

/**
 * Инициализация библиотеки AOS для анимаций при скролле
 */
function initAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
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

// Экспортируем функции для использования из HTML
window.openAppointmentModal = openAppointmentModal;
window.closeAppointmentModal = closeAppointmentModal;
window.openReviewModal = openReviewModal;
window.closeReviewModal = closeReviewModal;


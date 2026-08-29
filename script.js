// ==========================================================================
// ALI AKBAR HALA HANDICRAFT - CORE JAVASCRIPT
// ==========================================================================

const SHOP_PHONE = "923332583262"; // Shahzad Halai (Primary WhatsApp)
const SECONDARY_PHONE = "923342863986"; // Shiraz Halai
const CURRENCY = "Rs. ";

// Global Products State (populated dynamically from products.json)
let products = [];

// WhatsApp Routing - Round-Robin load balancer between Shahzad & Shiraz
function getCheckoutPhone() {
    const lastTarget = localStorage.getItem('lastCheckedOutPhone');
    
    // Alternate between the two phones to balance incoming orders
    const nextPhone = (lastTarget === SHOP_PHONE) ? SECONDARY_PHONE : SHOP_PHONE;
    localStorage.setItem('lastCheckedOutPhone', nextPhone);
    return nextPhone;
}

// Global Cart State from LocalStorage
let cart = JSON.parse(localStorage.getItem('aliAkbarCart')) || [];

// DOM Elements
const cartSidebar = document.getElementById('cart-sidebar');
const cartOverlay = document.getElementById('cart-overlay');
const cartIcon = document.getElementById('cart-icon');
const cartCount = document.getElementById('cart-count');
const closeCart = document.querySelector('.close-cart');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalPrice = document.getElementById('cart-total-price');
const cartGrandTotal = document.getElementById('cart-grand-total');
const checkoutBtn = document.getElementById('checkout-btn');

// Mobile Hamburger Navigation
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
}

// Scroll Animations using Intersection Observer
const observerOptions = {
    threshold: 0.05,
    rootMargin: "0px 0px -20px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

function applyAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in');
    animatedElements.forEach(el => {
        observer.observe(el);
        // Fallback timeout to ensure content is always visible
        setTimeout(() => el.classList.add('visible'), 400);
    });
}

// --- LIGHTBOX GALLERY ---
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const closeLightbox = document.querySelector('.close-lightbox');

function openLightbox(imageSrc) {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = imageSrc;
    lightbox.style.display = 'flex';
}

if (closeLightbox) {
    closeLightbox.addEventListener('click', () => {
        lightbox.style.display = 'none';
    });
}

// --- PRODUCT QUICK VIEW MODAL ---
const modal = document.getElementById('product-modal');
const closeModal = document.querySelector('.close-modal');
let currentProduct = null;

function openModal(productId) {
    if (!modal || typeof products === 'undefined') return;
    currentProduct = products.find(p => p.id === productId);
    if (!currentProduct) return;
    
    const modalImg = document.getElementById('modal-img');
    modalImg.src = currentProduct.image;
    modalImg.onerror = function() {
        this.src = "https://images.unsplash.com/photo-1621510488241-11d2797ce328?q=80&w=600&auto=format&fit=crop";
    };
    modalImg.onclick = () => openLightbox(currentProduct.image);
    
    // Multiple Images Gallery thumbnails rendering
    const thumbnailsContainer = document.getElementById('modal-thumbnails');
    if (thumbnailsContainer) {
        if (currentProduct.images && currentProduct.images.length > 1) {
            thumbnailsContainer.style.display = 'flex';
            thumbnailsContainer.innerHTML = currentProduct.images.map((img, idx) => `
                <button class="thumbnail-btn ${idx === 0 ? 'active' : ''}" data-index="${idx}" data-img="${img}" aria-label="View product image ${idx+1}">
                    <img src="${img}" onerror="this.src='https://images.unsplash.com/photo-1621510488241-11d2797ce328?q=80&w=200&auto=format&fit=crop';">
                </button>
            `).join('');
            
            const thumbnailBtns = thumbnailsContainer.querySelectorAll('.thumbnail-btn');
            thumbnailBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    thumbnailBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    
                    const selectedImg = btn.dataset.img;
                    modalImg.src = selectedImg;
                    modalImg.onclick = () => openLightbox(selectedImg);
                });
            });
        } else {
            thumbnailsContainer.style.display = 'none';
            thumbnailsContainer.innerHTML = '';
        }
    }
    
    document.getElementById('modal-title').textContent = currentProduct.name;
    document.getElementById('modal-price').textContent = `${CURRENCY}${currentProduct.price.toLocaleString()}`;
    document.getElementById('modal-desc').textContent = currentProduct.description;
    
    // Sizes Selector
    const sizeGroup = document.getElementById('size-group');
    const sizeSelect = document.getElementById('modal-size');
    if (currentProduct.sizes && currentProduct.sizes.length > 0) {
        sizeGroup.style.display = 'block';
        sizeSelect.innerHTML = currentProduct.sizes.map(s => `<option value="${s}">${s}</option>`).join('');
    } else {
        sizeGroup.style.display = 'none';
        sizeSelect.innerHTML = '';
    }
    
    // Colors Selector
    const colorGroup = document.getElementById('color-group');
    const colorSelect = document.getElementById('modal-color');
    if (currentProduct.colors && currentProduct.colors.length > 0) {
        colorGroup.style.display = 'block';
        colorSelect.innerHTML = currentProduct.colors.map(c => `<option value="${c}">${c}</option>`).join('');
    } else {
        colorGroup.style.display = 'none';
        colorSelect.innerHTML = '';
    }
    
    document.getElementById('modal-qty').value = 1;
    document.getElementById('modal-notes').value = '';
    
    modal.style.display = 'flex';
}

if (closeModal) {
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

// Global outside click handler
window.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
    if (e.target === lightbox) lightbox.style.display = 'none';
    if (e.target === cartOverlay) closeCartSidebar();
});

// --- CART MANAGEMENT ---
function saveCart() {
    localStorage.setItem('aliAkbarCart', JSON.stringify(cart));
    updateCartCount();
    renderCartItems();
}

function updateCartCount() {
    if (!cartCount) return;
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = count;
}

function getCartItemKey(product, size, color, notes) {
    return `${product.id}-${size || 'default'}-${color || 'default'}-${notes || 'none'}`;
}

const modalAddBtn = document.getElementById('modal-add-btn');
if (modalAddBtn) {
    modalAddBtn.addEventListener('click', () => {
        if (!currentProduct) return;
        
        const sizeGroup = document.getElementById('size-group');
        const colorGroup = document.getElementById('color-group');
        const size = sizeGroup && sizeGroup.style.display !== 'none' ? document.getElementById('modal-size').value : null;
        const color = colorGroup && colorGroup.style.display !== 'none' ? document.getElementById('modal-color').value : null;
        const qty = parseInt(document.getElementById('modal-qty').value) || 1;
        const notes = document.getElementById('modal-notes').value.trim();
        
        addToCartDirect(currentProduct, size, color, notes, qty);
        modal.style.display = 'none';
        openCartSidebar();
    });
}

function addToCartDirect(product, size = null, color = null, notes = '', qty = 1) {
    const cartKey = getCartItemKey(product, size, color, notes);
    const existingIndex = cart.findIndex(item => item.cartKey === cartKey);
    
    if (existingIndex > -1) {
        cart[existingIndex].quantity += qty;
    } else {
        cart.push({
            cartKey,
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            size,
            color,
            notes,
            quantity: qty
        });
    }
    
    saveCart();
}

function openCartSidebar() {
    if (!cartSidebar || !cartOverlay) return;
    cartSidebar.classList.add('open');
    cartOverlay.classList.add('active');
    renderCartItems();
}

function closeCartSidebar() {
    if (!cartSidebar || !cartOverlay) return;
    cartSidebar.classList.remove('open');
    cartOverlay.classList.remove('active');
}

if (cartIcon) {
    cartIcon.addEventListener('click', (e) => {
        e.preventDefault();
        openCartSidebar();
    });
}

if (closeCart) {
    closeCart.addEventListener('click', closeCartSidebar);
}

function renderCartItems() {
    if (!cartItemsContainer) return;
    cartItemsContainer.innerHTML = '';
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart-state">
                <i class="fa-solid fa-bag-shopping"></i>
                <p style="font-size:1.1rem; font-weight:600; color:var(--dark-espresso);">Your shopping cart is empty.</p>
                <p style="font-size:0.9rem; margin-top:4px;">Explore our 290+ Hala handicrafts to add items!</p>
            </div>
        `;
        if (cartTotalPrice) cartTotalPrice.textContent = `${CURRENCY}0`;
        if (cartGrandTotal) cartGrandTotal.textContent = `${CURRENCY}0`;
        return;
    }
    
    let total = 0;
    
    cart.forEach((item, index) => {
        total += item.price * item.quantity;
        
        let metaHtml = '';
        if (item.size) metaHtml += `<span>Size: ${item.size}</span> `;
        if (item.color) metaHtml += `<span>Color: ${item.color}</span>`;
        if (item.notes) metaHtml += `<br><small style="color:var(--terracotta);">Note: "${item.notes}"</small>`;
        
        const cartItemEl = document.createElement('div');
        cartItemEl.className = 'cart-item';
        cartItemEl.innerHTML = `
            <img src="${item.image}" alt="${item.name}" onerror="this.src='https://images.unsplash.com/photo-1621510488241-11d2797ce328?q=80&w=400&auto=format&fit=crop';">
            <div class="cart-item-details">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-meta">${metaHtml}</div>
                <div class="cart-item-price">${CURRENCY}${(item.price * item.quantity).toLocaleString()}</div>
                <div class="cart-item-controls">
                    <button class="cart-qty-btn" data-action="update-qty" data-index="${index}" data-delta="-1">-</button>
                    <span style="font-weight:600; font-size:0.9rem; padding: 0 4px;">${item.quantity}</span>
                    <button class="cart-qty-btn" data-action="update-qty" data-index="${index}" data-delta="1">+</button>
                    <span class="cart-item-remove" data-action="remove-item" data-index="${index}">
                        <i class="fa-regular fa-trash-can"></i> Remove
                    </span>
                </div>
            </div>
        `;
        cartItemsContainer.appendChild(cartItemEl);
    });
    
    if (cartTotalPrice) {
        cartTotalPrice.textContent = `${CURRENCY}${total.toLocaleString()}`;
    }
    if (cartGrandTotal) {
        cartGrandTotal.textContent = `${CURRENCY}${total.toLocaleString()}`;
    }
}

// Attach cart interactions listener
if (cartItemsContainer) {
    cartItemsContainer.addEventListener('click', (e) => {
        const target = e.target.closest('[data-action]');
        if (!target) return;
        
        const action = target.dataset.action;
        const index = parseInt(target.dataset.index);
        
        if (action === 'update-qty') {
            const delta = parseInt(target.dataset.delta);
            updateQty(index, delta);
        } else if (action === 'remove-item') {
            removeFromCart(index);
        }
    });
}

function updateQty(index, delta) {
    if (cart[index]) {
        cart[index].quantity += delta;
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
        saveCart();
    }
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
}

// WhatsApp Order Checkout
if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
        if (cart.length === 0) {
            alert("Your cart is empty! Please add some products first.");
            return;
        }
        
        let message = `السلام علیکم! 🛍️ *New Order from Website*\n`;
        message += `*Store:* Ali Akbar Hala Handicraft (علي اکبر ھالا ھينڊي کرافٽس)\n`;
        message += `------------------------------------\n\n`;
        
        let total = 0;
        
        cart.forEach((item, index) => {
            message += `*${index + 1}. ${item.name}*\n`;
            message += `• Price: ${CURRENCY}${item.price.toLocaleString()} x ${item.quantity} = *${CURRENCY}${(item.price * item.quantity).toLocaleString()}*\n`;
            if (item.size) message += `• Size: ${item.size}\n`;
            if (item.color) message += `• Color: ${item.color}\n`;
            if (item.notes) message += `• Special Note: ${item.notes}\n`;
            if (item.image) {
                const baseOrigin = window.location.origin;
                const imgPath = item.image.startsWith('/') ? item.image : `/${item.image}`;
                message += `• Image Link: ${baseOrigin}${imgPath}\n`;
            }
            message += `\n`;
            total += item.price * item.quantity;
        });
        
        message += `------------------------------------\n`;
        message += `💰 *Grand Total Amount:* *${CURRENCY}${total.toLocaleString()}*\n\n`;
        message += `📍 *Delivery Address / Name:* [Please write your name & address here]\n`;
        message += `Please confirm my order and availability. Thank you!`;
        
        const encoded = encodeURIComponent(message);
        window.open(`https://wa.me/${getCheckoutPhone()}?text=${encoded}`, '_blank');
    });
}

// --- PRODUCT GRID, PAGINATION & SEARCH FILTERING ---
const productGrid = document.getElementById('product-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const searchInput = document.getElementById('product-search');
const loadMoreContainer = document.getElementById('load-more-container');
const loadMoreBtn = document.getElementById('load-more-btn');

let currentCategory = 'all';
let searchQuery = '';
let visibleCount = 24; // Show 24 items per batch
const BATCH_SIZE = 24;

function getFilteredProducts() {
    if (typeof products === 'undefined' || !Array.isArray(products)) {
        return [];
    }
    return products.filter(product => {
        const matchesCategory = (currentCategory === 'all' || product.category === currentCategory);
        const matchesSearch = !searchQuery || 
            product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (product.categoryLabel && product.categoryLabel.toLowerCase().includes(searchQuery.toLowerCase())) ||
            (product.description && product.description.toLowerCase().includes(searchQuery.toLowerCase()));
            
        return matchesCategory && matchesSearch;
    });
}

function renderProducts(resetCount = true) {
    if (!productGrid || typeof products === 'undefined') return;
    
    if (resetCount) {
        visibleCount = document.body.classList.contains('home-page') ? 8 : BATCH_SIZE;
        productGrid.innerHTML = '';
    }
    
    const filtered = getFilteredProducts();
    const itemsToDisplay = filtered.slice(0, visibleCount);
    
    if (resetCount) {
        productGrid.innerHTML = '';
    }
    
    if (filtered.length === 0) {
        productGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem;">
                <i class="fa-solid fa-magnifying-glass" style="font-size: 3rem; color: var(--border-light); margin-bottom: 1rem;"></i>
                <h3 style="color: var(--dark-espresso); margin-bottom: 0.5rem;">No handicrafts found</h3>
                <p style="color: var(--text-muted);">Try a different keyword or choose another category.</p>
            </div>
        `;
        if (loadMoreContainer) loadMoreContainer.style.display = 'none';
        return;
    }
    
    // Clear and re-append
    productGrid.innerHTML = '';
    itemsToDisplay.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card fade-in visible';
        card.innerHTML = `
            ${product.badge ? `<span class="product-badge">${product.badge}</span>` : ''}
            <div class="product-img-wrapper" data-action="open-modal" data-id="${product.id}">
                <img src="${product.image}" alt="${product.name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1621510488241-11d2797ce328?q=80&w=400&auto=format&fit=crop';">
                <div class="product-quick-view">
                    <span class="quick-view-btn"><i class="fa-regular fa-eye"></i> Quick View</span>
                </div>
            </div>
            <div class="product-info">
                <span class="product-category">${product.categoryLabel || 'Hala Handicraft'}</span>
                <h3 class="product-title" data-action="open-modal" data-id="${product.id}" style="cursor:pointer;" title="${product.name}">${product.name}</h3>
                <div class="product-price-row">
                    <span class="product-currency">${CURRENCY}</span>
                    <span class="product-price">${product.price.toLocaleString()}</span>
                </div>
                <div class="product-actions">
                    <button class="btn btn-primary" data-action="open-modal" data-id="${product.id}">
                        <i class="fa-solid fa-cart-shopping"></i> Order / Details
                    </button>
                </div>
            </div>
        `;
        productGrid.appendChild(card);
        observer.observe(card);
    });
    
    // Attach product grid modal listeners via event delegation
    if (productGrid && !productGrid.dataset.listenerAttached) {
        productGrid.addEventListener('click', (e) => {
            const modalTrigger = e.target.closest('[data-action="open-modal"]');
            if (modalTrigger) {
                const productId = parseInt(modalTrigger.dataset.id);
                openModal(productId);
            }
        });
        productGrid.dataset.listenerAttached = 'true';
    }
    
    // Load More Visibility
    if (loadMoreContainer) {
        if (visibleCount < filtered.length && !document.body.classList.contains('home-page')) {
            loadMoreContainer.style.display = 'block';
            loadMoreBtn.innerHTML = `<i class="fa-solid fa-spinner"></i> Load More Products (${filtered.length - visibleCount} remaining)`;
        } else {
            loadMoreContainer.style.display = 'none';
        }
    }
}

// Load More Click Handler
if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
        visibleCount += BATCH_SIZE;
        renderProducts(false);
    });
}

// Search Input Listener
if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
        searchQuery = e.target.value.trim();
        renderProducts(true);
    }, 250));
}

// Filter Buttons Click
if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.filter;
            renderProducts(true);
        });
    });
}

// Custom Order Form Submission
const customOrderForm = document.getElementById('custom-order-form');
if (customOrderForm) {
    customOrderForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const name = document.getElementById('custom-name').value;
        const details = document.getElementById('custom-details').value;
        
        let message = `السلام علیکم! ✨ *Custom Order / Inquiry*\n`;
        message += `*Store:* Ali Akbar Hala Handicraft\n\n`;
        message += `*Customer Name:* ${name}\n`;
        message += `*Inquiry Details:* ${details}\n\n`;
        message += `Please let me know the rates and availability. Thank you!`;
        
        const encoded = encodeURIComponent(message);
        window.open(`https://wa.me/${getCheckoutPhone()}?text=${encoded}`, '_blank');
        customOrderForm.reset();
    });
}

// --- UTILITY FUNCTIONS ---
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Sync cart pricing and existence with database
function syncCartWithCatalog() {
    if (typeof products === 'undefined' || !Array.isArray(products) || products.length === 0) return;
    
    let cartModified = false;
    
    // Filter cart to only keep items that exist in catalog, and update their prices
    cart = cart.filter(item => {
        const catalogItem = products.find(p => p.id === item.id);
        if (!catalogItem) {
            // Discontinued item - remove
            cartModified = true;
            return false;
        }
        
        if (item.price !== catalogItem.price) {
            // Price updated - update cart item price
            item.price = catalogItem.price;
            cartModified = true;
        }
        return true;
    });
    
    if (cartModified) {
        saveCart();
    }
}

// --- INITIALIZATION ---
async function loadProducts() {
    try {
        const response = await fetch('products.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        products = await response.json();
        
        // Sync Cart pricing & items with newly loaded products database
        syncCartWithCatalog();
        
        // Update product count UI elements
        const prodCount = products.length;
        const countAllEl = document.getElementById('count-all');
        if (countAllEl) {
            countAllEl.textContent = prodCount;
        }
        const navCountEl = document.getElementById('nav-product-count');
        if (navCountEl) {
            navCountEl.textContent = prodCount;
        }
        
        // Check URL parameters for category filtering (e.g. shop.html?cat=kashi)
        const urlParams = new URLSearchParams(window.location.search);
        const catParam = urlParams.get('cat');
        if (catParam) {
            currentCategory = catParam;
            const filterBtns = document.querySelectorAll('.filter-btn');
            if (filterBtns.length > 0) {
                filterBtns.forEach(btn => {
                    if (btn.dataset.filter === catParam) {
                        filterBtns.forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                    }
                });
            }
        }
        
        // Render products if layout includes product grid
        const productGrid = document.getElementById('product-grid');
        if (productGrid) {
            renderProducts(true);
        }
    } catch (err) {
        console.error("Failed to load products.json:", err);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    applyAnimations();
    
    // Dynamic Navbar active state selection based on current file/page name
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinksEls = document.querySelectorAll('.nav-links a');
    navLinksEls.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Load products asynchronously
    loadProducts();
    
    // Swiper Hero Slider Initialization
    if (typeof Swiper !== 'undefined' && document.querySelector('.swiper')) {
        document.querySelectorAll('.swiper').forEach(swiperEl => {
            new Swiper(swiperEl, {
                loop: true,
                speed: 900,
                autoplay: {
                    delay: 4500,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: swiperEl.querySelector('.swiper-pagination') || '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: swiperEl.querySelector('.swiper-button-next') || '.swiper-button-next',
                    prevEl: swiperEl.querySelector('.swiper-button-prev') || '.swiper-button-prev',
                },
                effect: 'fade',
                fadeEffect: {
                    crossFade: true
                }
            });
        });
    }
});

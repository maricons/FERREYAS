/**
 * Funciones para el carrito de compras de Ferremas
 */

// Controlador para la cantidad
function setupQuantityControls() {
    const quantityInput = document.getElementById('quantity');
    if (!quantityInput) return;
    
    const decreaseBtn = document.getElementById('decrease-quantity');
    const increaseBtn = document.getElementById('increase-quantity');
    
    decreaseBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
    
    increaseBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue < 99) {
            quantityInput.value = currentValue + 1;
        }
    });
    
    // Validar entrada manual
    quantityInput.addEventListener('change', function() {
        let currentValue = parseInt(quantityInput.value);
        if (isNaN(currentValue) || currentValue < 1) {
            quantityInput.value = 1;
        } else if (currentValue > 99) {
            quantityInput.value = 99;
        }
    });
}

// Añadir al carrito
async function addToCart() {
    // Agregar event listeners a todos los botones de añadir al carrito
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            
            if (!productId) {
                console.error('No se encontró el ID del producto');
                return;
            }
            
            const isLoggedIn = document.getElementById('user-status')?.value === 'true';
            
            if (!isLoggedIn) {
                window.location.href = '/login';
                return;
            }
            
            try {
                const requestData = {
                    product_id: parseInt(productId),
                    quantity: 1
                };
                
                console.log('Enviando datos al carrito:', requestData);
                
                const response = await fetch('/api/cart/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                
                const responseData = await response.json();
                console.log('Respuesta del servidor:', responseData);
                
                if (!response.ok) {
                    throw new Error(responseData.error || 'Error al añadir al carrito');
                }
                
                // Mostrar mensaje de éxito
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
                alertDiv.style.zIndex = '1050';
                alertDiv.innerHTML = `
                    <i class="fas fa-check-circle me-2"></i>${productName} añadido al carrito
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                document.body.appendChild(alertDiv);
                
                // Actualizar contador del carrito
                await updateCartCount();
                
                // Remover el mensaje después de 3 segundos
                setTimeout(() => {
                    alertDiv.remove();
                }, 3000);
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error al añadir el producto al carrito: ' + error.message);
            }
        });
    });
}

// Cargar el carrito completo
async function loadCart() {
    try {
        const response = await fetch('/api/cart');
        
        // Si la respuesta no es exitosa (ej. no autenticado), mostrar carrito vacío
        if (!response.ok) {
            if (document.getElementById('cart-items')) {
                const emptyCartMessage = document.getElementById('empty-cart-message');
                const checkoutBtn = document.getElementById('checkout-btn');
                
                if (emptyCartMessage) {
                    emptyCartMessage.style.display = 'block';
                }
                if (checkoutBtn) {
                    checkoutBtn.disabled = true;
                }
                
                updateCartTotals(0, 0, 0);
            }
            return [];
        }
        
        const cartItems = await response.json();
        
        // Actualizar la UI solo si estamos en la página del carrito
        if (document.getElementById('cart-items')) {
            updateCartUI(cartItems);
        }
        
        return cartItems;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// Actualizar la interfaz del carrito
function updateCartUI(cartItems) {
    const cartItemsContainer = document.getElementById('cart-items');
    if (!cartItemsContainer) return;
    
    const emptyCartMessage = document.getElementById('empty-cart-message');
    const checkoutBtn = document.getElementById('checkout-btn');
    
    if (cartItems.length === 0) {
        if (emptyCartMessage) {
            emptyCartMessage.style.display = 'block';
        }
        if (checkoutBtn) {
            checkoutBtn.disabled = true;
        }
        updateCartTotals(0, 0, 0);
        return;
    }
    
    if (emptyCartMessage) {
        emptyCartMessage.style.display = 'none';
    }
    if (checkoutBtn) {
        checkoutBtn.disabled = false;
    }
    
    let cartHTML = '';
    let total = 0;
    
    cartItems.forEach(item => {
        const product = item.product;
        let priceToShow = product.price;
        let priceHtml = '';
        // Si el producto está en promoción, mostrar ambos precios
        if (product.is_promotion && product.promotion_price !== null && product.promotion_price !== undefined) {
            priceToShow = product.promotion_price;
            priceHtml = `<span class="text-decoration-line-through text-muted">$${product.price.toLocaleString('es-CL')}</span> <span class="text-danger ms-2">$${product.promotion_price.toLocaleString('es-CL')}</span>`;
        } else {
            priceHtml = `<span class="h5 mb-0">$${product.price.toLocaleString('es-CL')}</span>`;
        }
        const itemTotal = item.quantity * priceToShow;
        total += itemTotal;
        
        // Preparar la URL de la imagen correctamente
        let imgSrc = product.image;
        if (imgSrc && !imgSrc.startsWith('http') && !imgSrc.startsWith('/static/')) {
            imgSrc = `/static/images/products/${imgSrc}`;
        }
        
        cartHTML += `
            <div class="cart-item" data-id="${item.id}">
                <div class="row align-items-center">
                    <div class="col-md-2">
                        <img src="${imgSrc}" class="img-fluid" alt="${product.name}" onerror="this.src='/static/images/products/no-image.jpg'">
                    </div>
                    <div class="col-md-4">
                        <h5>${product.name}</h5>
                        <p class="text-muted">Precio: ${priceHtml}</p>
                    </div>
                    <div class="col-md-3">
                        <div class="quantity-control">
                            <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                            <input type="number" value="${item.quantity}" min="1" max="99" 
                                   onchange="updateQuantity(${item.id}, this.value)">
                            <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <strong>$${itemTotal.toLocaleString('es-CL')}</strong>
                    </div>
                    <div class="col-md-1">
                        <button class="btn btn-sm btn-danger" onclick="removeItem(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    cartItemsContainer.innerHTML = cartHTML;
    
    // Calcular subtotal e IVA (el precio ya incluye IVA)
    const subtotal = Math.round(total / 1.19);
    const tax = total - subtotal;
    updateCartTotals(subtotal, tax, total);
}

// Actualizar totales del carrito
function updateCartTotals(subtotal, tax, total) {
    const subtotalElement = document.getElementById('cart-subtotal');
    if (!subtotalElement) return;
    
    subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('cart-tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('cart-total').textContent = `$${total.toFixed(2)}`;
}

// Actualizar cantidad de un producto en el carrito
async function updateQuantity(itemId, newQuantity) {
    if (newQuantity < 1) newQuantity = 1;
    if (newQuantity > 99) newQuantity = 99;
    
    try {
        const response = await fetch(`/api/cart/update/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: parseInt(newQuantity) }),
        });
        
        if (!response.ok) {
            throw new Error('Error al actualizar la cantidad');
        }
        
        // Verificar si estamos en la página del carrito antes de intentar recargar la vista
        const isCartPage = document.getElementById('cart-items') !== null;
        if (isCartPage) {
            await loadCart();
        }
        
        // Actualizar contador del carrito (esto funciona en todas las páginas)
        await updateCartCount();
    } catch (error) {
        console.error('Error:', error);
    }
}

// Eliminar un producto del carrito
async function removeItem(itemId) {
    if (!confirm('¿Estás seguro de eliminar este producto del carrito?')) {
        return;
    }
    
    try {
        // Mostrar indicador de carga o deshabilitar el botón para feedback visual
        const deleteButton = document.querySelector(`.cart-item[data-id="${itemId}"] .btn-danger`);
        if (deleteButton) {
            deleteButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            deleteButton.disabled = true;
        }
        
        const response = await fetch(`/api/cart/remove/${itemId}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }
        
        // Verificar si estamos en la página del carrito
        const isCartPage = document.getElementById('cart-items') !== null;
        if (isCartPage) {
            // Eliminar el elemento directamente del DOM con animación
            const cartItem = document.querySelector(`.cart-item[data-id="${itemId}"]`);
            if (cartItem) {
                // Agregar efecto de desvanecimiento
                cartItem.style.transition = 'all 0.3s ease';
                cartItem.style.opacity = '0';
                cartItem.style.maxHeight = '0';
                cartItem.style.margin = '0';
                cartItem.style.padding = '0';
                cartItem.style.overflow = 'hidden';
                
                // Después de la animación, eliminar el elemento y actualizar totales
                setTimeout(async () => {
                    cartItem.remove();
                    
                    // Recalcular totales
                    const cartItems = await fetch('/api/cart').then(r => r.json());
                    if (cartItems.length === 0) {
                        const emptyCartMessage = document.getElementById('empty-cart-message');
                        const checkoutBtn = document.getElementById('checkout-btn');
                        
                        if (emptyCartMessage) {
                            emptyCartMessage.style.display = 'block';
                        }
                        if (checkoutBtn) {
                            checkoutBtn.disabled = true;
                        }
                        
                        updateCartTotals(0, 0, 0);
                    } else {
                        // Calcular nuevos totales
                        let total = 0;
                        cartItems.forEach(item => {
                            total += item.quantity * item.product.price;
                        });
                        
                        // Calcular subtotal e IVA (el precio ya incluye IVA)
                        const subtotal = Math.round(total / 1.19);
                        const tax = total - subtotal;
                        updateCartTotals(subtotal, tax, total);
                    }
                }, 300);
            }
        }
        
        // Actualizar contador del carrito en todas las páginas
        await updateCartCount();
    } catch (error) {
        console.error('Error:', error);
        // Restaurar el botón si hay un error
        const deleteButton = document.querySelector(`.cart-item[data-id="${itemId}"] .btn-danger`);
        if (deleteButton) {
            deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
            deleteButton.disabled = false;
        }
    }
}

// Actualizar el contador del carrito
async function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (!cartCountElement) return;
    
    try {
        const response = await fetch('/api/cart');
        // Si no estamos autenticados o hay otro error, ocultar el contador
        if (!response.ok) {
            cartCountElement.style.display = 'none';
            return;
        }
        
        const cartItems = await response.json();
        const count = cartItems.reduce((total, item) => total + item.quantity, 0);
        
        if (count > 0) {
            cartCountElement.textContent = count > 9 ? '9+' : count;
            cartCountElement.style.display = 'flex';
        } else {
            cartCountElement.style.display = 'none';
        }
    } catch (error) {
        console.error('Error al cargar el conteo del carrito:', error);
        cartCountElement.style.display = 'none';
    }
}

// Iniciar proceso de pago con Webpay
async function iniciarPago() {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    loadingOverlay.innerHTML = `
        <div style="background: white; padding: 20px; border-radius: 5px; text-align: center;">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Procesando pago...</p>
        </div>
    `;
    
    try {
        // Mostrar overlay de carga
        document.body.appendChild(loadingOverlay);
        
        console.log('Iniciando proceso de pago...');
        
        const response = await fetch('/iniciar-pago', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('Respuesta recibida:', response);

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error en la respuesta:', errorData);
            throw new Error(errorData.error || 'Error al iniciar el pago');
        }

        const data = await response.json();
        console.log('Datos de redirección recibidos:', data);
        
        if (!data.token || !data.url) {
            console.error('Datos de redirección inválidos:', data);
            throw new Error('Datos de redirección inválidos');
        }

        console.log('Redirigiendo a:', data.url);
        
        // Crear un formulario oculto para enviar el token a Webpay
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = data.url;
        form.style.display = 'none';
        
        // Agregar el token como token_ws
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'token_ws';
        tokenInput.value = data.token;
        
        form.appendChild(tokenInput);
        document.body.appendChild(form);
        
        // Enviar el formulario
        console.log('Enviando formulario a Webpay...');
        form.submit();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Ha ocurrido un error al procesar el pago. Por favor, intente nuevamente.');
        // Remover overlay de carga en caso de error
        loadingOverlay.remove();
    }
}

// Inicializar todas las funcionalidades
document.addEventListener('DOMContentLoaded', async function() {
    // Inicializar controles de cantidad
    setupQuantityControls();
    
    // Inicializar botón de añadir al carrito
    //addToCart();
    
    // Cargar el carrito si estamos en la página del carrito
    if (document.getElementById('cart-items')) {
        await loadCart();
        
        // Inicializar el botón de checkout
        const checkoutBtn = document.getElementById('checkout-btn');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', iniciarPago);
        }
    }
    
    // Actualizar contador del carrito en todas las páginas
    await updateCartCount();
}); 
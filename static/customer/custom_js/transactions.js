
// Global state

(() => {
    const state = {
        search: '',
        dateFrom: '',
        dateTo: '',
        status: '',
        orderBy: 'desc',
        perPage: '10',
        exportFormat: '',
        exportMethod: '',
        statementStyle: 'modern',
        loading: false
    };

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Bootstrap tooltips/popovers if needed
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Set default date range (last 30 days)
        setDefaultDateRange();

        // Check CSRF token
        checkCSRFToken();

        // Keyboard shortcut for debug panel
        document.addEventListener('keydown', function (e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                toggleDebug();
            }
        });

        // Close modals on escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                });
            }
        });
    });

    // Set default date range (last 30 days)
    function setDefaultDateRange() {
        const today = new Date();
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(today.getDate() - 30);

        const formatDate = (date) => {
            return date.toISOString().split('T')[0];
        };

        document.getElementById('dateFrom').value = formatDate(thirtyDaysAgo);
        document.getElementById('dateTo').value = formatDate(today);

        state.dateFrom = formatDate(thirtyDaysAgo);
        state.dateTo = formatDate(today);
    }

    // Check CSRF token presence
    function checkCSRFToken() {
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        const statusEl = document.getElementById('csrfStatus');
        if (statusEl) {
            statusEl.textContent = csrfMeta ? '✓ Present' : '✗ Missing';
            statusEl.className = csrfMeta ? 'text-success fw-medium' : 'text-danger fw-medium';
        }
    }

    // Toggle debug panel
    function toggleDebug() {
        const panel = document.getElementById('debugPanel');
        panel.classList.toggle('d-none');
    }

    // Handle search input
    function handleSearch(value) {
        state.search = value.trim();
        // Debounce search - implement your filtering logic here
        debounce(() => {
            console.log('Searching for:', state.search);
            // fetchTransactions(); // Call your API
        }, 300)();
    }

    // Debounce utility
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Apply filters from modal
    function applyFilters() {
        state.dateFrom = document.getElementById('dateFrom').value;
        state.dateTo = document.getElementById('dateTo').value;
        state.status = document.getElementById('statusFilter').value;
        state.orderBy = document.getElementById('orderBy').value;
        state.perPage = document.getElementById('perPage').value;

        // Close modal
        const modalEl = document.getElementById('filterModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();

        // Apply filters - implement your API call here
        console.log('Applying filters:', state);
        // fetchTransactions();

        // Show feedback
        showTemporaryMessage('Filters applied', 'success');
    }

    // Select statement style
    function selectStyle(style, element) {
        state.statementStyle = style;

        // Update UI
        document.querySelectorAll('.style-option').forEach(el => {
            el.classList.remove('selected');
        });
        element.classList.add('selected');
    }

    // Handle export action
    async function handleExport() {
        const format = document.getElementById('exportFormat').value;
        const method = document.getElementById('exportMethod').value;

        // Validation
        if (!format || !method) {
            showTemporaryMessage('Please select both format and delivery method', 'danger');
            return;
        }

        state.exportFormat = format;
        state.exportMethod = method;

        const exportBtn = document.getElementById('exportBtn');
        const originalBtnContent = exportBtn.innerHTML;

        try {
            // Show loading state
            exportBtn.disabled = true;
            exportBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span>Processing...';

            // Handle "view" method - open in new tab
            if (method === 'view') {
                const url = new URL("{% url 'customer:dashboard' %}", window.location.origin);
                url.searchParams.append('exportType', format);
                url.searchParams.append('exportAs', method);
                url.searchParams.append('statementStyle', state.statementStyle);

                // Add filters
                if (state.dateFrom) url.searchParams.append('startDate', state.dateFrom);
                if (state.dateTo) url.searchParams.append('endDate', state.dateTo);
                if (state.status) url.searchParams.append('status', state.status);

                window.open(url.toString(), '_blank', 'width=800,height=1000,resizable=yes,scrollbars=yes');
                closeModal('exportModal');
                return;
            }

            // Prepare form data for POST
            const formData = new FormData();
            formData.append('exportType', format);
            formData.append('exportAs', method);
            formData.append('statementStyle', state.statementStyle);
            if (state.dateFrom) formData.append('dateFrom', state.dateFrom);
            if (state.dateTo) formData.append('dateTo', state.dateTo);
            if (state.status) formData.append('status', state.status);

            // Get CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }

            if (method === 'download') {
                // Direct download via form submission
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = "{% url 'customer:dashboard' %}";
                form.style.display = 'none';

                // Add CSRF
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = '_token';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                // Add fields
                for (const [key, value] of formData.entries()) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = value;
                    form.appendChild(input);
                }

                document.body.appendChild(form);
                form.submit();
                document.body.removeChild(form);

            } else if (method === 'email') {
                // Email export via fetch
                const response = await fetch("{% url 'customer:dashboard' %}", {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': csrfToken,
                        'Accept': 'application/json'
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    showTemporaryMessage('Export sent to your email', 'success');
                } else {
                    throw new Error(data.message || 'Export failed');
                }
            }

            // Close modal and reset
            closeModal('exportModal');
            showTemporaryMessage('Export started successfully', 'success');

        } catch (error) {
            console.error('Export error:', error);
            showTemporaryMessage(error.message || 'An error occurred during export', 'danger');
        } finally {
            // Reset button
            exportBtn.disabled = false;
            exportBtn.innerHTML = originalBtnContent;
        }
    }

    // Close modal by ID
    function closeModal(modalId) {
        const modalEl = document.getElementById(modalId);
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
    }

    // Show temporary message (toast-style)
    function showTemporaryMessage(text, type = 'info') {
        // Create or get toast container
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '1100';
            document.body.appendChild(container);
        }

        // Create toast
        const toastId = 'toast-' + Date.now();
        const bgClass = {
            'success': 'bg-success',
            'danger': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        }[type] || 'bg-primary';

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white ${bgClass} border-0`;
        toast.id = toastId;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${text}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        container.appendChild(toast);

        // Show and auto-hide
        const bsToast = new bootstrap.Toast(toast, { delay: 4000 });
        bsToast.show();

        // Cleanup after hide
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    // Test export endpoint (debug)
    async function testExportEndpoint() {
        const resultEl = document.getElementById('testResult');
        resultEl.textContent = 'Testing...';
        resultEl.className = 'mt-2 small text-primary';

        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
            if (!csrfToken) {
                throw new Error('CSRF token missing');
            }

            const response = await fetch("{% url 'customer:dashboard' %}", {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': csrfToken,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ test: true })
            });

            if (response.ok) {
                resultEl.textContent = `✓ Success! Status: ${response.status}`;
                resultEl.className = 'mt-2 small text-success fw-medium';
            } else {
                resultEl.textContent = `✗ Error: Status ${response.status}`;
                resultEl.className = 'mt-2 small text-danger fw-medium';
            }
        } catch (error) {
            resultEl.textContent = `✗ Error: ${error.message}`;
            resultEl.className = 'mt-2 small text-danger fw-medium';
        }
    }

    // Optional: Fetch transactions from API
    async function fetchTransactions() {
        try {
            const params = new URLSearchParams();
            if (state.search) params.append('search', state.search);
            if (state.dateFrom) params.append('date_from', state.dateFrom);
            if (state.dateTo) params.append('date_to', state.dateTo);
            if (state.status) params.append('status', state.status);
            params.append('order_by', state.orderBy);
            params.append('per_page', state.perPage);

            const response = await fetch(`{% url 'customer:dashboard' %}?${params}`);
            const data = await response.json();

            // Render transactions
            renderTransactions(data.results || []);

        } catch (error) {
            console.error('Failed to fetch transactions:', error);
            showTemporaryMessage('Failed to load transactions', 'danger');
        }
    }

    // Render transactions table
    function renderTransactions(transactions) {
        const tbody = document.getElementById('transactionsBody');

        if (!transactions || transactions.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="empty-state">
                        <i class="bi bi-inbox empty-icon"></i>
                        <p class="empty-title">No transactions found</p>
                        <p class="empty-text">Try adjusting your search or filter parameters</p>
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = transactions.map(txn => `
            <tr>
                <td><i class="bi bi-chevron-right text-muted small"></i></td>
                <td>
                    <span class="${txn.amount >= 0 ? 'amount-credit' : 'amount-debit'}">
                        ${txn.amount >= 0 ? '+' : ''}${formatCurrency(txn.amount)}
                    </span>
                </td>
                <td>${txn.type || 'Transfer'}</td>
                <td>
                    ${txn.status === 'COMPLETED'
                ? '<span class="badge-completed"><i class="bi bi-check-circle-fill"></i> Completed</span>'
                : '<span class="badge-pending"><i class="bi bi-clock"></i> Pending</span>'
            }
                </td>
                <td><code class="small">${txn.reference || 'N/A'}</code></td>
                <td class="text-truncate" style="max-width: 200px;" title="${txn.description || ''}">
                    ${txn.description || '-'}
                </td>
                <td>${txn.scope || 'Local'}</td>
                <td>${formatDate(txn.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary" onclick="viewTransaction('${txn.id}')">
                        View
                    </button>
                </td>
            </tr>
        `).join('');

        // Reinitialize icons if using Lucide
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    // Format currency
    function formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(Math.abs(amount));
    }

    // Format date
    function formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

})();

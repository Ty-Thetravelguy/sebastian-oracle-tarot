$(document).ready(function() {
    // Initialize materialize components
    M.AutoInit();

    // Date picker initialization
    $('.datepicker').datepicker({
        format: 'd mmm, yyyy', // Set the date format
        yearRange: [new Date().getFullYear() - 80, new Date().getFullYear()] // Set the year range
    }).attr('readonly', 'readonly'); // Make the datepicker field readonly

    // Time picker initialization
    $('.timepicker').timepicker({
        twelveHour: true // Use 12-hour format
    }).attr('readonly', 'readonly'); // Make the timepicker field readonly

    // Open date picker on focus
    $('#date_of_birth').on('focus', function() {
        $(this).datepicker('open');
    });

    // Open time picker on focus
    $('#time_of_birth').on('focus', function() {
        $(this).timepicker('open');
    });

    // Manually handle closing of the time picker
    $(document).on('click', '.timepicker-close, .btn-flat', function() {
        const timePickerInstance = M.Timepicker.getInstance($('#time_of_birth'));
        if (timePickerInstance) {
            timePickerInstance.close();
        }
    });

    // Password match and requirements check logic
    function validatePassword() {
        const password = $('#password').val();
        const passwordRepeat = $('#password_repeat').val();
        const passwordMessage = $('#password_message');
        const matchMessage = $('#password_match_message');
        const requirementsPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\\|,.<>\/?]).{6,20}$/;

        if (!requirementsPattern.test(password)) {
            passwordMessage.text('Password must be between 6 and 20 characters long, contain at least one uppercase letter, one number, and one special character. (!@#$%^&*()_+\-=\[\]{};:\\|,.<>\/?)').css('color', '#fafafa');
        } else {
            passwordMessage.text('');
        }

        if (password !== passwordRepeat) {
            matchMessage.text('Passwords do not match').css('color', '#fafafa');
        } else {
            matchMessage.text('Passwords match').css('color', '#fafafa');
        }
    }

    $('#password, #password_repeat').on('input', validatePassword);

    // Password hover logic
    $('#password, #password_repeat').hover(function() {
        $(this).attr('title', 'Password must be between 6 and 20 characters long, contain at least one uppercase letter, one number, and one special character.');
    });

    // Form submission logic
    $('#tarot-form').on('submit', function(event) {
        const password = $('#password').val();
        const passwordRepeat = $('#password_repeat').val();
        const requirementsPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\\|,.<>\/?]).{6,20}$/;

        // Check if passwords match and meet requirements
        if (password !== passwordRepeat || !requirementsPattern.test(password)) {
            event.preventDefault();
            alert('Passwords do not match or do not meet the requirements. Please try again.');
            return false;
        }

        // Save form data to local storage
        const form = event.target;
        const formData = new FormData(form);
        localStorage.setItem('tarot_choice', formData.get('tarot_choice'));
        localStorage.setItem('question', formData.get('question'));

        // Redirect to loading page
        window.location.href = '/loading';
    });

    // Load tarot reading data
    if (window.location.pathname === '/reading') {
        const data = localStorage.getItem('tarotReadingData');
        console.log("Loaded tarot reading data from localStorage:", data); // Debug log

        if (data) {
            const parsedData = JSON.parse(data);
            if (parsedData && parsedData.selected_cards) {
                const cardContainer = $('#cards-container');
                cardContainer.empty(); // Clear previous content if any
                parsedData.selected_cards.forEach((card, index) => {
                    if (index % 3 === 0) {
                        cardContainer.append('<div class="row card-row"></div>');
                    }
                    const cardElement = $(`
                        <div class="col s12 m4">
                            <div class="card">
                                <div class="card-image">
                                    <img src="${card.cardImg}" alt="${card.cardName}" class="responsive-img">
                                </div>
                                <div class="card-content">
                                    <p class="center-align blue-grey-text text-darken-4">${card.cardName}</p>
                                </div>
                            </div>
                        </div>
                    `);
                    cardContainer.find('.row').last().append(cardElement);
                });
                $('#reading-output').text(parsedData.reading_output);
                $('#shuffling-image').hide(); // Hide the shuffling image
                $('#cards-container').show();
                $('#reading-result').show();
            } else {
                console.error("Tarot reading data is missing or malformed:", parsedData); // Debug log
                alert('An error occurred while loading your tarot reading. Please try again.');
            }
        } else {
            console.error("No tarot reading data found in localStorage."); // Debug log
            alert('An error occurred while loading your tarot reading. Please try again.');
        }
    }

    // Handle tarot reading processing on the loading page
    if (window.location.pathname === '/loading') {
        fetch('/process_tarot_reading', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tarot_choice: localStorage.getItem('tarot_choice'),
                question: localStorage.getItem('question')
            })
        }).then(response => {
            return response.json();
        }).then(data => {
            if (data.success) {
                localStorage.setItem('tarotReadingData', JSON.stringify(data));
                window.location.href = '/reading';
            } else {
                alert('An error occurred while processing your request. Please try again.');
                window.location.href = '/';
            }
        }).catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while processing your request. Please try again.');
            window.location.href = '/';
        });
    }

    // Clear form logic
    $('#tarot-form').on('reset', function() {
        // Clear the form fields
        $(this).find('input[type=text], textarea').val('');
        // Reset the select element
        $(this).find('select').prop('selectedIndex', 0).formSelect();
        // Clear local storage items related to the form
        localStorage.removeItem('tarot_choice');
        localStorage.removeItem('question');
    });
});

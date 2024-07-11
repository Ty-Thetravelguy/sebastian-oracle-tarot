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

    /**
     * Validates the password fields and displays appropriate messages.
     */
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

    /**
     * Handles form submission for the tarot form.
     * @param {Event} event - The form submission event.
     */
    $('#tarot-form').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        const form = event.target;
        const formData = new FormData(form);

        // Save form data to local storage
        localStorage.setItem('tarot_choice', formData.get('tarot_choice'));
        localStorage.setItem('question', formData.get('question'));

        // Set session data
        fetch('/set_tarot_choice_and_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tarot_choice: formData.get('tarot_choice'),
                question: formData.get('question')
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Redirect to loading page
                  window.location.href = '/loading';
              } else {
                  alert('Failed to set tarot choice and question.');
              }
          })
          .catch((error) => {
              console.error('Error:', error);
              alert('An error occurred while setting tarot choice and question. Please try again.');
          });
    });

    /**
     * Loads tarot reading data from local storage and displays it on the reading page.
     */
    if (window.location.pathname === '/reading') {
        const data = localStorage.getItem('tarotReadingData');
    
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
                        <div class="col s4">
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
                    cardContainer.find('.card-row').last().append(cardElement);
                });
                $('#reading-output').text(parsedData.reading_output);
    
            } else {
                console.error("Tarot reading data is missing or malformed:", parsedData);
                alert('An error occurred while loading your tarot reading. Please try again.');
            }
        } else {
            console.error("No tarot reading data found in localStorage.");
            alert('An error occurred while loading your tarot reading. Please try again.');
        }
    }

    /**
     * Handles tarot reading processing on the loading page.
     */
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
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  localStorage.setItem('tarotReadingData', JSON.stringify(data));
                  window.location.href = '/reading';
              } else {
                  alert(data.message || 'Please login or register.');
                  window.location.href = '/login';
              }
          }).catch((error) => {
              console.error('Error:', error);
              alert('An error occurred while processing your request. Please try again.');
              window.location.href = '/';
          });
    }

    /**
     * Clears the tarot form fields and local storage items related to the form.
     */
    $('#tarot-form').on('reset', function() {
        // Clear the form fields
        $(this).find('input[type=text], textarea').val('');
        // Reset the select element
        $(this).find('select').prop('selectedIndex', 0).formSelect();
        // Clear local storage items related to the form
        localStorage.removeItem('tarot_choice');
        localStorage.removeItem('question');
    });

    /**
     * Initializes collapsible components for saved readings page.
     */
    if (window.location.pathname === '/saved_readings') {
        $('.collapsible').collapsible();
        $('.journal-btn').on('click', function() {
            // Redirect to the journal page
            window.location.href = '/journal';
        });
    }

    /**
     * Handles saving a tarot reading.
     */
    $('#save-reading-btn').on('click', function() {
        const readingDate = new Date().toLocaleDateString();
        const questionAsked = localStorage.getItem('question');
        const readingData = $('#reading-output').text();
        const category = localStorage.getItem('tarot_choice'); // Add this line to get the tarot choice

        fetch('/save_reading', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                readingDate: readingDate,
                questionAsked: questionAsked,
                readingData: readingData,
                category: category // Include category in the payload
            })
        }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Reading saved successfully.');
                    window.location.href = data.redirect_url; // Redirect to saved readings page
                } else {
                    alert('Error saving reading: ' + data.message);
                }
            }).catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while saving your reading. Please try again.');
            });
    });

    /**
     * Handles deleting a tarot reading.
     */
    let readingToDelete = null;
    $(document).on('click', '.delete-reading-btn', function() {
        readingToDelete = $(this).data('reading-id');
        $('#delete-modal').modal('open');
    });

    /**
     * Confirms and deletes the selected tarot reading.
     */
    $('#confirm-delete-btn').on('click', function() {
        const confirmationInput = $('#delete-confirmation').val();
        if (readingToDelete && confirmationInput === 'DELETE') {
            fetch('/delete_reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    readingId: readingToDelete
                })
            }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Reading and journal deleted successfully.');
                        location.reload(); // Reload the page to update the list
                    } else {
                        alert('Error deleting reading: ' + data.message);
                    }
                }).catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting your reading. Please try again.');
                });
        } else {
            alert('Please type DELETE to confirm.');
        }
    });

    /**
     * Enables the confirm delete button only if the input is "DELETE".
     */
    $('#delete-confirmation').on('input', function() {
        const confirmationInput = $(this).val();
        if (confirmationInput === 'DELETE') {
            $('#confirm-delete-btn').removeAttr('disabled');
        } else {
            $('#confirm-delete-btn').attr('disabled', 'disabled');
        }
    });

    /**
     * Saves a journal entry related to a tarot reading.
     */
    $(document).on('click', '.save-journal-btn', function() {
        const readingId = $(this).data('reading-id');
        const journalSubject = $(`#journal-subject-${readingId}`).val();
        const journalDate = $(`#journal-date-${readingId}`).val();
        const journalText = $(`#journal-text-${readingId}`).val();

        fetch('/save_journal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                readingId: readingId,
                journalSubject: journalSubject,
                journalDate: journalDate,
                journalText: journalText
            })
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Journal entry saved successfully.');
            } else {
                alert('Error saving journal entry: ' + data.message);
            }
        }).catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while saving your journal entry. Please try again.');
        });
    });

    /**
     * Handles deleting a journal entry.
     */
    let journalToDelete = null;
    $(document).on('click', '.delete-journal-btn', function() {
        journalToDelete = $(this).data('reading-id');
        $('#delete-journal-modal').modal('open');
    });

    /**
     * Confirms and deletes the selected journal entry.
     */
    $('#confirm-delete-journal-btn').on('click', function() {
        if (journalToDelete) {
            fetch('/delete_journal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    readingId: journalToDelete
                })
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Journal entry deleted successfully.');
                    location.reload(); // Reload the page to update the list
                } else {
                    alert('Error deleting journal entry: ' + data.message);
                }
            }).catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while deleting your journal entry. Please try again.');
            });
        }
    });

    /**
     * Handles account deletion process.
     */
    $('.delete-account-btn').on('click', function() {
        $('#delete-account-modal').modal('open');
    });

    /**
     * Enables the confirm delete account button only if the input is "DELETE".
     */
    $('#delete-account-confirmation').on('input', function() {
        const confirmationInput = $(this).val();
        if (confirmationInput === 'DELETE') {
            $('#confirm-delete-account-btn').removeAttr('disabled');
        } else {
            $('#confirm-delete-account-btn').attr('disabled', 'disabled');
        }
    });

    /**
     * Confirms and deletes the user's account.
     */
    $('#confirm-delete-account-btn').on('click', function() {
        const confirmationInput = $('#delete-account-confirmation').val();
        if (confirmationInput === 'DELETE') {
            fetch('/delete_account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Account deleted successfully.');
                    window.location.href = data.redirect_url; // Redirect to login page
                } else {
                    alert('Error deleting account: ' + data.message);
                }
            }).catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while deleting your account. Please try again.');
            });
        } else {
            alert('Please type DELETE to confirm.');
        }
    });

});

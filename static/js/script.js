$(document).ready(function() {
    // Initialize materialize components
    M.AutoInit();

    // Form submission logic
    $('#tarot-form').on('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        // Save form data to local storage
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
});

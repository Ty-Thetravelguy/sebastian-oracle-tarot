$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: 'dd mmm, yyyy', 
        yearRange: 60 
    });
    $('.timepicker').timepicker();
});

$(document).ready(function() {
    // Initialize materialize components
    M.AutoInit();

    // Form submission logic
    $('#tarot-form').on('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        
        console.log("Form submitted with data:", formData); // Debug log

        $.ajax({
            url: '/tarot_reading',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log("AJAX success, data received:", data); // Debug log
                localStorage.setItem('tarotReadingData', JSON.stringify(data));
                window.location.href = '/reading';
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error); // Debug log
                alert('An error occurred while processing your request. Please try again.');
            }
        });
    });

    // Load tarot reading data
    if (window.location.pathname === '/reading') {
        setTimeout(function() {
            $('#shuffling-image').hide();
            const data = localStorage.getItem('tarotReadingData');
            console.log("Loaded tarot reading data from localStorage:", data); // Debug log

            if (data) {
                const parsedData = JSON.parse(data);
                if (parsedData && parsedData.selected_cards) {
                    const cardContainer = $('#cards-container');
                    parsedData.selected_cards.forEach(card => {
                        const cardElement = $(`
                            <div class="col s4 m2">
                                <img src="${card.cardImg}" alt="${card.cardName}" class="responsive-img">
                                <p class="center-align grey-text text-lighten-5">${card.cardName}</p>
                            </div>
                        `);
                        cardContainer.append(cardElement);
                    });
                    $('#reading-output').text(parsedData.reading_output);
                    $('#reading-result').show();
                } else {
                    console.error("Tarot reading data is missing or malformed:", parsedData); // Debug log
                    alert('An error occurred while loading your tarot reading. Please try again.');
                }
            } else {
                console.error("No tarot reading data found in localStorage."); // Debug log
                alert('An error occurred while loading your tarot reading. Please try again.');
            }
        }, 10000); // 10 seconds
    }
});

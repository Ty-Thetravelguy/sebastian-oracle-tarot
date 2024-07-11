# Sebastian Oracle's - Milestone Project 3 

## HTML, CSS, JavaScript, Python+Flask and MongoDB - Back End Development

Enter a realm of mysticism and wonder with Sebastian Oracle's tarot reading app. With over a decade of experience, Sebastian Oracle now unveils his craft to the World Wide Web, offering you profound insights into your life's journey. The app features three distinctive spreads, each tailored to your specific enquiries:

General Life Enquiry (Three-Card Spread):
- **Reason:** Gain a holistic view of your life's many facets, understanding the interplay of various elements.
- **User Interaction:** Inquire, "What is the overall state of my life right now?" 
- **App functionality:** Three cards are drawn to capture your existence's essence.

Work/Career Enquiry (Five-Card Spread):
- **Reason:** Navigate the currents of your career, uncovering past influences, present challenges, and future prospects.
- **User Interaction:** Pose the question, "What can I expect in my career?" and draw 
- **App functionality:** Five cards drawn to illuminate your professional path.

Love Enquiry (Six-Card Spread):
- **Reason:** Delve into the tapestry of your romantic past, present, and future.
- **User Interaction:** Ask, "What should I know about my love life?" 
- **App functionality:** Six cards will be drawn to reveal the hidden truths of your heart.

Each reading is enriched with personalised insights drawn from the user's name, date of birth, time of birth, and birth location, which are stored in the user profile. These details weave a deeper connection between the querent and the cosmic energies at play, offering a reading that's uniquely theirs. The app integrates astrological wisdom, identifying life patterns and significant transitions, enhancing the tarot's mystical guidance.

As you journey through your reading, the app allows you to save your insights and journal your reflections. This feature helps you express your thoughts and feelings, fostering a deeper understanding and personal growth. Embrace the mystery, and let Sebastian Oracle guide you through the whispers of the tarot.

## Table of contents

1. [Business Needs](#business-needs)

2. [User Wants](#user-wants)

## Business Needs

### Business Needs:

1.	Market Differentiation:

-   Create a unique and engaging user experience that sets the app apart from other online tarot reading services.
-   Incorporate a blend of traditional tarot practices and modern technology to attract a broad audience.

2.	User Engagement:

-   Develop features that encourage regular use, such as daily tarot cards, personalized notifications, and seasonal promotions.
-   Create a community aspect with forums or social sharing options to increase user interaction and retention.

3.	Data Security and Privacy:

-   Ensure robust security measures to protect user data, particularly sensitive information like birth details.
-   Comply with data protection regulations to build user trust and maintain the app’s reputation.

### Future Development Business Wants:

1.	Revenue Generation:

-   Implement a pricing model that includes in-app purchases, subscription plans, or pay-per-reading options.
-   Offer premium features such as personalised readings, in-depth astrological insights, and detailed reports to increase revenue.

2.	Scalability:

-   Design the app to handle a growing user base without compromising performance.
-   Plan for future updates and expansions, including additional spreads, new astrological features, and enhanced user interface elements.

3.	Brand Development:

-   Promote Sebastian Oracle's brand through strategic marketing campaigns, including social media, influencer partnerships, and content marketing.
-   Foster a loyal user base through excellent customer support and regular engagement initiatives.

## User Wants:

1.	Accurate and Insightful Readings:

-   Provide tarot readings that users feel are accurate and insightful, offering real value and guidance.
-   Integrate astrological data to enhance the depth and personalisation of each reading.

2.	Ease of Use:

-   Design an intuitive and user-friendly interface that makes navigation and interaction straightforward and enjoyable.
-   Ensure the process of entering personal information and accessing readings is simple and hassle-free.

3.	Personalization:

-   Allow users to save their profiles with personal details to receive more tailored readings.
-   Offer options to store past readings and journal their thoughts for future reflection.

4.	Privacy and Security:

-   Guarantee that personal information, such as birth details and reading history, is kept confidential and secure.
-   Provide clear information on how user data is used and protected.

### Future Development User Wants:

1.	Engagement and Interactivity:

-   Include features that encourage users to engage with the app regularly, such as daily horoscopes or card pulls.
-   Offer interactive elements like the ability to share readings or participate in community discussions.
-   Pull their own cards and do their own readings. 

2.	Support and Guidance:

-   Provide access to resources that help users understand and interpret their readings better, such as guides or tutorials.
-   Ensure there is customer support available to assist with any questions or technical issues.
-   Links to other support such as mental health and crisis management.

3.	Flexibility:

-   Offer various reading options and spreads to cater to different questions and concerns users might have.
-   Allow users to choose the depth and detail of their readings, from quick insights to comprehensive analyses.

# Manual Testing Checklist

## User Registration
1. **Can a user register with valid information?**
   - Yes, the user can register successfully with valid information.
2. **What happens if a user tries to register with an email that already exists?**
   - The system displays an error message indicating that the email is already in use.
3. **Is there a validation message for passwords that do not meet the required criteria?**
   - Yes, a validation message is displayed if the password does not meet the criteria.
4. **Does the system prevent registration if the passwords do not match?**
   - Yes, the system prevents registration and displays a message indicating the passwords do not match.
5. **Is a success message displayed upon successful registration?**
   - Yes, a success message is displayed upon successful registration.
6. **Is the user redirected to the home page after successful registration?**
   - Yes, the user is redirected to the home page after successful registration.

## User Login
1. **Can a user login with valid credentials?**
   - Yes, the user can login with valid credentials.
2. **What happens if a user tries to login with an incorrect email?**
   - An error message is displayed indicating that the email is incorrect.
3. **What happens if a user tries to login with an incorrect password?**
   - An error message is displayed indicating that the password is incorrect.
4. **Is there a validation message if either the email or password fields are empty?**
   - Yes, a validation message is displayed if either the email or password fields are empty.
5. **Is a success message displayed upon successful login?**
   - Yes, a success message is displayed upon successful login.
6. **Is the user redirected to the home page after successful login?**
   - Yes, the user is redirected to the home page after successful login.

## User Profile
1. **Can a logged-in user view their profile?**
   - Yes, a logged-in user can view their profile.
2. **Is the profile information displayed correctly?**
   - Yes, the profile information is displayed correctly.
3. **What happens if a non-logged-in user tries to access the profile page?**
   - The non-logged-in user is redirected to the login page.
4. **Can a user update their email address?**
   - Yes, a user can update their email address.
5. **What happens if a user tries to update their email to an already existing one?**
   - The system displays an error message indicating that the email is already in use.

## Tarot Reading Process
1. **Can a user select a tarot choice and ask a question?**
   - Yes, a user can select a tarot choice and ask a question.
2. **Is the tarot_choice and question correctly set in the session?**
   - Yes, the tarot_choice and question are correctly set in the session.
3. **Does the loading page process the tarot reading correctly?**
   - Yes, the loading page processes the tarot reading correctly.
4. **Is the tarot reading result displayed correctly on the reading page?**
   - Yes, the tarot reading result is displayed correctly on the reading page.
5. **What happens if there is no tarot_choice or question set in the session?**
   - The system displays an error message or prompts the user to select a tarot choice and ask a question.

## Saved Readings
1. **Can a logged-in user view their saved readings?**
   - Yes, a logged-in user can view their saved readings.
2. **Is the saved readings list displayed correctly with all details?**
   - Yes, the saved readings list is displayed correctly with all details.
3. **Can a user save a tarot reading?**
   - Yes, a user can save a tarot reading.
4. **Is there a success message displayed upon saving a reading?**
   - Yes, a success message is displayed upon saving a reading.
5. **Can a user delete a saved reading?**
   - Yes, a user can delete a saved reading.
6. **Is there a confirmation prompt before deleting a reading?**
   - Yes, there is a confirmation prompt before deleting a reading.
7. **Is there a success message displayed upon successful deletion?**
   - Yes, a success message is displayed upon successful deletion.

## Journal Entries
1. **Can a user add a journal entry to a saved reading?**
   - Yes, a user can add a journal entry to a saved reading.
2. **Is there a success message displayed upon saving a journal entry?**
   - Yes, a success message is displayed upon saving a journal entry.
3. **Can a user edit a journal entry?**
   - Yes, a user can edit a journal entry.
4. **Can a user delete a journal entry?**
   - Yes, a user can delete a journal entry.
5. **Is there a confirmation prompt before deleting a journal entry?**
   - Yes, there is a confirmation prompt before deleting a journal entry.
6. **Is there a success message displayed upon successful deletion of a journal entry?**
   - Yes, a success message is displayed upon successful deletion of a journal entry.

## Account Management
1. **Can a user delete their account?**
   - Yes, a user can delete their account.
2. **Is there a confirmation prompt before deleting the account?**
   - Yes, there is a confirmation prompt before deleting the account.
3. **Is there a success message displayed upon successful account deletion?**
   - Yes, a success message is displayed upon successful account deletion.
4. **Is the user redirected to the login page after account deletion?**
   - Yes, the user is redirected to the login page after account deletion.
5. **Are all saved readings and journal entries associated with the deleted account also deleted?**
   - Yes, all saved readings and journal entries associated with the deleted account are also deleted.

## Miscellaneous
1. **Does the date picker and time picker work correctly on the registration and profile update forms?**
   - Yes, the date picker and time picker work correctly on the registration and profile update forms.
2. **Are form fields cleared when the form is reset?**
   - Yes, form fields are cleared when the form is reset.
3. **Are validation messages correctly displayed and styled?**
   - Yes, validation messages are correctly displayed and styled.
4. **Are all user inputs sanitized to prevent XSS attacks?**
   - Yes, all user inputs are sanitized to prevent XSS attacks.
5. **Are all buttons and links functioning and redirecting correctly?**
   - Yes, all buttons and links are functioning and redirecting correctly.

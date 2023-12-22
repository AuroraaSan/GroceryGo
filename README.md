# GroceryGo Store

Welcome to the GitHub repository for GroceryGo, an advanced web application designed to revolutionize the online grocery shopping experience. Utilizing web development technologies and database integration, particularly the Django framework, GroceryGo offers a comprehensive and user-friendly platform for grocery shopping.

![GroceryGo](https://github.com/AuroraaSan/GroceryGo/blob/main/static/logoo.png)
## Live Version
Visit the live version of GroceryGo: [GroceryGo Live Website](https://grocery-go-24-b1f88daa13b9.herokuapp.com/)

## Key Features

### User Authentication and Management
- **User Registration and Login:** Unique credentials for user registration and login, ensuring secure and personalized accounts.
- **Password Reset:** Users can reset their password via email for enhanced security.
- **User Profile Management:** Personalized user profiles for managing additional data like multiple addresses.
- **Address Management:** A dedicated table for addresses with a one-to-many relationship to users, allowing selection of different addresses for each order.

### Shopping Cart Database
- **Personalized Shopping Carts:** A dedicated database table for user shopping carts, recording items, quantities, and total cost for each user.
- **Cart Management:** Users can view, update, add, or delete items in their shopping cart and apply coupons before placing an order.

### Grocery Listing and Filtering
- **Comprehensive Product Database:** A database for all available products, categorized by company and brand, with detailed product information.
- **Advanced Filtering and Search:** Users can filter groceries by price range, company, and brand nationality. The majority of products are 100% Egyptian.

### Purchase Analytics
- **Insightful Analytics:** The website provides valuable data on purchasing trends and consumer behavior like how many customers ordered the product in general and in the last 24 hours.
  
### Secure Online Payment with Stripe
- **Stripe Payment Integration:** GroceryGo utilizes Stripe for secure, efficient online payment processing, enabling easy transactions with credit and debit cards.

## Technologies Used

### Web Development
- **Frontend:** The user interface is built using HTML and CSS, providing a responsive and visually appealing design that enhances user experience.
- **Backend:** The application logic is powered by Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design.

### Database Integration
- **Initial Database:** The project initially used SQLite, a lightweight and efficient database engine perfect for development and testing.
- **Current Database:** Migrated to PostgreSQL for its scalability, and advanced features, better suited for managing larger datasets and ensuring improved performance in production environments.

## ERD for database
![ER Diagram](https://github.com/AuroraaSan/GroceryGo/blob/main/static/img/ERD.png)


### Payment Processing
- **Stripe:** Integrated Stripe for secure and efficient online payment processing. Stripe API is used for handling transactions, offering a seamless checkout experience for users.

### Hosting and Deployment
- **Heroku:** The application is deployed on Heroku, a cloud platform service that enables easy scaling and maintenance of web applications. Heroku’s support for containerization and integration with GitHub provides a streamlined deployment process.
  
## Contributors

- **Ahmed Haggag** [LinkedIn Profile]([https://www.linkedin.com/in/arwa-alorbany/](https://www.linkedin.com/in/ahmed-hagag-28698514b/))
- **Arwa Zakaria Khaled Alorbany** [LinkedIn Profile]([https://www.linkedin.com/in/arwa-alorbany/](https://www.linkedin.com/in/arwazakaria20/))
- **Mariam Ahmed Sheta** [LinkedIn Profile]([https://www.linkedin.com/in/arwa-alorbany/](https://www.linkedin.com/in/mariam-sheta-gogo/))
- **Youssef Ashraf Elharty** [LinkedIn Profile]([https://www.linkedin.com/in/arwa-alorbany/](https://www.linkedin.com/in/youssefelharty/)https://www.linkedin.com/in/youssefelharty/)

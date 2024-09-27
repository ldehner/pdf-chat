# PDF Chat System

This project is a **PDF-based chat system** where administrators can upload PDFs and generate vector embeddings for them. Users can then interact with a chat interface to ask questions about specific PDFs. The system uses embeddings to understand and retrieve relevant sections of the PDF to answer the user's questions.

## Features

- **Admin & User roles**: 
  - Admins can upload multiple PDFs.
  - Normal users can engage in chats but cannot upload PDFs.
- **Embeddings**: 
  - Each PDF is broken into multiple sections or chunks, and embeddings are generated for each chunk using vector-based models.
  - These embeddings are stored in a PostgreSQL database using the `pgvector` extension.
- **Chat functionality**: 
  - Users can ask questions, and the system will identify the relevant PDF and generate answers based on the content of the embeddings.
  - Each user can have multiple chats, and each chat can have multiple messages (questions and answers).
  
## Database Schema

The database schema uses PostgreSQL and is designed as follows:

### User
- `id`: UUID
- `name`: STRING
- `password`: STRING
- `isAdmin`: BOOLEAN (determines if the user is an admin)
- Relationships: 
  - A user can upload multiple PDFs (if admin).
  - A user can have multiple chats.

### PDF
- `id`: UUID
- `name`: STRING
- `user_id`: UUID (foreign key referencing the User who uploaded the PDF)
- Relationships: 
  - A PDF can have multiple embeddings.

### Embedding
- `id`: UUID
- `pdf_id`: UUID (foreign key referencing the PDF)
- `vector`: PGVECTOR (the embedding vector representing sections of the PDF)

### Chat
- `id`: UUID
- `user_id`: UUID (foreign key referencing the User)
- `title`: STRING (the title of the chat)
- `last_updated`: TIMESTAMP (auto-updated on new messages)
- Relationships: 
  - A chat can have multiple messages.

### Message
- `id`: UUID
- `timestamp`: TIMESTAMP
- `question`: STRING (user's question)
- `answer`: STRING (system's response based on the PDF)
- `chat_id`: UUID (foreign key referencing the chat)

## Technology Stack

- **Backend**: Python (with SQLAlchemy ORM for database management)
- **Frontend**: Angular
- **Database**: PostgreSQL (with pgvector extension for embeddings)
- **Embeddings**: Generated from PDF chunks using vector models (e.g., BERT or other transformer-based models)
- **Authentication**: Role-based system with Admin and User roles

## How It Works

1. **Admin Upload**: 
   - Admin is the first user who was registered
   - Admins upload PDFs, and the system processes the PDF into smaller chunks. 
   - Embeddings (vectors) are generated for each chunk and stored in the PostgreSQL database.

2. **User Chat**: 
   - Users can start a chat session where they ask questions about a PDF.
   - The system compares the question's embedding with the stored PDF embeddings and retrieves relevant sections to generate an answer.

3. **Storing Chats**:
   - Each user can create multiple chat sessions. 
   - For each session, the user's questions and the system's answers are stored as individual messages.

## Startup instructions
Here is a markdown instruction on how to start the project and access the frontend:

## Project Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Services Overview
This `docker-compose.yml` sets up three services:
1. **API**: A FastAPI backend service that runs on port `8000`.
2. **Frontend**: An Angular app served by Nginx, accessible on port `4200`.
3. **PostgreSQL**: A PostgreSQL database using the `ankane/pgvector` image with the `pgvector` extension.

### Steps to Start the Project

1. **Clone the repository** (if not done already):
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Ensure the folder structure is correct**:
   - Backend code should be in `./backend`.
   - Frontend Angular app should be in `./frontend/pdf-chat`.
   - The `init.sql` file (to initialize the database) should be in `./backend/database/init.sql`.

3. **Build and Start the Containers**:
   Run the following command to build and start all the containers (backend, frontend, and database):

   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the FastAPI backend (`api`).
   - Build and serve the Angular frontend (`frontend`).
   - Start the PostgreSQL database with the `pgvector` extension.

4. **Access the Frontend**:
   Once the containers are up and running, you can access the Angular frontend via the following URL:

   ```
   http://localhost:4200
   ```

5. **Access the Backend API**:
   You can access the FastAPI backend by visiting:

   ```
   http://localhost:8000
   ```

### Stopping the Containers
To stop the containers, run:

```bash
docker-compose down
```

This will stop and remove all the running containers.

### Notes:
- The PostgreSQL service is configured to use the `pgvector` extension.
- The health check ensures the API only starts after the PostgreSQL service is ready.


## Future Improvements

- **Authentication & Authorization**: Implement secure authentication for users and admins.
- **Search Optimization**: Fine-tune the model used for embeddings to improve the accuracy of answers.
- **File Formats**: Extend support to other document formats like Word or HTML.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

This README is generated

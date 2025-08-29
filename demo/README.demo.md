# Chatbot Theme Identifier Demo Script Docs

This is a demo script docs meant to give a demo of how the chatbot FastAPI works.

How to use the demo scripts:

 1. Run the `python3 demo_setup.py` command in your terminal. This script creates a text file and stores it into the `sample_docs` folder.
 2. Next run the FastAPI script with this command `fastapi run ./chatbot_theme_identifier/backend/app/main.py --host 0.0.0.0 --port 8080`.
 3. Finally, run `python3 demo_script.py`. 

If everything goes well, you will get an output like this in your terminal:

```markdown
Document Research & Theme Identification Chatbot Demo
================================================================================

Checking API health...
✓ API is running
✓ Uploaded 3 documents successfully
╭────────────────────────────────────────────────────── Question ──────────────────────────────────────────────────────╮
│                                                                                                                      │
│  Q: What are the main themes across all documents?                                                                   │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────────────── Document Answers ──────────────────────────────────────────────────╮
│ DOC001 (Page 14, Para 1)                                                                                             │
│ The main themes across all documents are:                                                                            │
│ 1.  The importance of just application of law.                                                                       │
│ 2.  The impact of new laws making the US voting and registration process more difficult.                             │
│ 3.  Natural Language Processing (NLP) and machine learning, specifically focusing on attention mechanisms in neural  │
│ networks, anaphora resolution, and machine translation.                                                              │
│                                                                                                                      │
│ DOC002 (Page 1, Para 6)                                                                                              │
│ The main themes are Machine Learning & Data Science, Software Development, Soft Skills, and Languages.               │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── Identified Themes ──────────────────────────────────────────────────╮
│ Artificial Intelligence and Data Science                                                                             │
│ This theme encompasses advanced computational techniques and their applications, specifically focusing on machine    │
│ learning, natural language processing (NLP), and data science. It includes concepts like neural networks, attention  │
│ mechanisms, anaphora resolution, and machine translation, highlighting the development and application of            │
│ intelligent systems.                                                                                                 │
│                                                                                                                      │
│ Legal and Societal Impact of Laws                                                                                    │
│ This theme centers on the critical examination of legal frameworks and their real-world consequences, particularly   │
│ concerning the fair and just application of law. It highlights the impact of new legislation, such as those          │
│ affecting the US voting and registration process, on civic participation and societal fairness.                      │
│                                                                                                                      │
│ Software Engineering and Professional Competencies                                                                   │
│ This theme broadly covers the technical and interpersonal skills essential for professional development in the       │
│ technology sector. It includes core software development practices, the cultivation of soft skills (e.g.,            │
│ communication, collaboration), and proficiency in various languages (presumably programming languages or human       │
│ languages relevant to tech roles).                                                                                   │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────── Question ──────────────────────────────────────────────────────╮
│                                                                                                                      │
│  Q: What are the key findings from these documents?                                                                  │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────────────── Document Answers ──────────────────────────────────────────────────╮
│ DOC003 (Page 1, Para 1)                                                                                              │
│ The document describes itself as a sample text file designed to demonstrate a chatbot's capabilities. Key findings   │
│ are that the document serves to illustrate the chatbot's ability to extract, process, index, and use text to answer  │
│ questions and identify themes, including across multiple document formats like plain text and PDFs.                  │
│                                                                                                                      │
│ DOC001 (Page 9, Para 1)                                                                                              │
│ The key findings are:                                                                                                │
│ 1.  **Transformer architecture effectiveness:** The Transformer, based entirely on attention, can be trained         │
│ significantly faster than recurrent or convolutional layer-based architectures for translation tasks.                │
│ 2.  **State-of-the-art performance:** It achieves new state-of-the-art results on WMT 2014 English-to-German and     │
│ English-to-French translation tasks, outperforming even previously reported ensembles.                               │
│ 3.  **Generalization to other tasks:** The Transformer generalizes well to English constituency parsing, performing  │
│ surprisingly well and outperforming many prior models, including the BerkeleyParser, even with smaller training      │
│ data.                                                                                                                │
│ 4.  **Architectural parameter insights:**                                                                            │
│     *   Varying attention heads: Both too few (single-head) and too many attention heads can negatively impact       │
│ quality.                                                                                                             │
│     *   Attention key size (`dk`): Reducing `dk` hurts model quality, suggesting the need for more sophisticated     │
│ compatibility functions.                                                                                             │
│     *   Model size: Bigger models generally perform better.                                                          │
│     *   Dropout: Very helpful in preventing overfitting.                                                             │
│     *   Positional encoding: Learned positional embeddings perform similarly to sinusoidal positional encoding.      │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── Identified Themes ──────────────────────────────────────────────────╮
│ Advancements in NLP Model Architectures                                                                              │
│ This theme focuses on the innovation and specific design principles behind cutting-edge Natural Language Processing  │
│ (NLP) models. DOC001 details the Transformer architecture, highlighting its novelty as an attention-based model, its │
│ ability to train significantly faster, and insights derived from its architectural parameters (like attention head   │
│ count, key size, and the importance of dropout). While DOC003 demonstrates an NLP application, it doesn't delve into │
│ the underlying model architecture, making DOC001 the sole document directly supporting this theme.                   │
│                                                                                                                      │
│ Demonstrated AI Capabilities and Applications                                                                        │
│ This theme encompasses the practical functionalities and real-world uses of AI and NLP technologies. DOC003 directly │
│ showcases a chatbot's capabilities, including its ability to extract, process, index text, answer questions, and     │
│ identify themes across various document formats. Similarly, DOC001 illustrates the Transformer's advanced            │
│ capabilities by achieving state-of-the-art results in complex tasks like machine translation and successfully        │
│ generalizing its performance to other NLP challenges such as English constituency parsing. Both documents provide    │
│ concrete examples of what AI systems can accomplish.                                                                 │
│                                                                                                                      │
│ Performance, Efficiency, and Generalization of AI Systems                                                            │
│ This theme highlights the operational strengths of modern AI models in terms of speed, accuracy, and adaptability.   │
│ DOC001 emphasizes the Transformer's "significantly faster" training times and its achievement of "new                │
│ state-of-the-art results," alongside its crucial ability to "generalize well" to different NLP tasks. DOC003         │
│ demonstrates the robustness and effective performance of a chatbot, specifically mentioning its capability to        │
│ process and utilize text to answer questions and identify themes "across multiple document formats," underscoring    │
│ its versatility and reliable operation in diverse data environments.                                                 │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────── Question ──────────────────────────────────────────────────────╮
│                                                                                                                      │
│  Q: Summarize the similarities between these documents.                                                              │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────────────── Document Answers ──────────────────────────────────────────────────╮
│ DOC002 (Page 1, Para 12)                                                                                             │
│ The professional certificates listed are all obtained from Udemy and relate to Deep Learning, Data Science, and      │
│ Machine Learning using Python-based tools like PyTorch and TensorFlow.                                               │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── Identified Themes ──────────────────────────────────────────────────╮
│ Educational Platform                                                                                                 │
│ The professional certificates are consistently obtained from the online learning platform, Udemy. This indicates a   │
│ reliance on e-learning for professional development in the covered domains.                                          │
│                                                                                                                      │
│ Core Subject Areas                                                                                                   │
│ The certificates are centered around key domains within artificial intelligence and data analytics, specifically     │
│ Deep Learning, Data Science, and Machine Learning. This highlights a specialization in modern data-driven            │
│ technologies.                                                                                                        │
│                                                                                                                      │
│ Specific Technologies & Tools                                                                                        │
│ The skills acquired involve practical application using Python-based tools, with a particular emphasis on prominent  │
│ machine learning frameworks like PyTorch and TensorFlow. This points to proficiency in widely-used industry          │
│ standards for AI development.                                                                                        │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

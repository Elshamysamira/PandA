import re
import snowballstemmer


class Document:
    def __init__(self, lines):
        self.lines = lines

    def tokenize(self) -> list[str]: #tokenizes, lowercases and splits the text into individual words
        tokenized_text = self.lines.lower()
        nospecial_tokenized_text = re.sub(r'[^a-z ]+', '', tokenized_text)
        clean_tokenized_text = nospecial_tokenized_text.split(" ")
        stemmer = snowballstemmer.stemmer('english')
        stemmed_words = [stemmer.stemWord(word) for word in clean_tokenized_text]
        return stemmed_words

class Sonnet(Document):

    def __init__(self, data: dict, ):
        super().__init__(" ".join(data["lines"]))

        self.title = self.extract_sonnet_title(data['title'])
        self.author = data["author"]
        self.linecount = int(data["linecount"])
        self.id = self.extract_sonnet_id(data['title'])

    def extract_sonnet_title(self, title):
        title_parts = title.split(': ', 1)
        if len(title_parts) > 1:
            return title_parts[1].strip()
        else:
            return None
    def extract_sonnet_id(self, text):
        match = re.search(r'Sonnet (\d+):', text)
        if match:
            return int(match.group(1))
        else:
            return None

    def __str__(self):
        final_string = f"Sonnet {self.id}: {self.lines}"
        return final_string

class Query(Document):
    def __init__(self, query: str):
        super().__init__(query)

class Index(dict[str, set[int]]): #is the index of a word and creates word : index
    def __init__(self, documents: list[Sonnet]):
        super().__init__()
        self.documents = documents
        for document in documents:
            self.add(document)
    def add(self, document: Sonnet): #adds the tokens of a sonnet to the index which then makes a set of word : index
        tokens = document.tokenize()
        for token in tokens:
            if token not in self:
                self[token] = set()

            self[token].add(document.id)

    def search(self, query: Query) -> list[Sonnet]:
        query_tokens = query.tokenize()
        query_document_ids = []
        for token in query_tokens:
            query_document_ids.append(self.get(token))
        query_document_ids_final = query_document_ids[0].intersection(*query_document_ids[1:]) #these are all the document IDs from any query
        matched_sonnets = []
        for document in self.documents:
            if document.id in query_document_ids_final:
                matched_sonnets.append(document)
        return matched_sonnets
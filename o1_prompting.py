##  https://platform.openai.com/docs/guides/reasoning

from openai import OpenAI

client = OpenAI()

prompt = """
Instructions:
- Given the React component below, change it so that nonfiction books have red
  text. 
- Return only the code in your reply
- Do not include any additional formatting, such as markdown code blocks
- For formatting, use four space tabs, and do not allow any lines of code to 
  exceed 80 columns

const books = [
  { title: 'Dune', category: 'fiction', id: 1 },
  { title: 'Frankenstein', category: 'fiction', id: 2 },
  { title: 'Moneyball', category: 'nonfiction', id: 3 },
];

export default function BookList() {
  const listItems = books.map(book =>
    <li>
      {book.title}
    </li>
  );

  return (
    <ul>{listItems}</ul>
  );
}
"""

response = client.chat.completions.create(
    model="o1-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
            ],
        }
    ]
)

print(response.choices[0].message.content)


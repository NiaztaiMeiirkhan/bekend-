from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import markdown

# --- App Configuration ---
app = FastAPI()

# --- CORS Configuration ---
origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://your-frontend-domain.vercel.app",  # Vercel domain
    "https://your-frontend-domain.netlify.app",  # Netlify domain
    "*"  # Production үшін барлық домендерді рұқсат ету (қауіпсіздік үшін нақты домендерді көрсетіңіз)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class PostBase(BaseModel):
    slug: str
    title: str
    author: str
    date: str
    category: str

class PostFull(PostBase):
    content: str
    content_html: str

# --- In-Memory Database ---
fake_posts_db: List[PostFull] = [
    PostFull(
        slug="first-post",
        title="Менің алғашқы постым",
        author="Айжан Құрманбекова",
        date="2024-01-15",
        category="Технология",
        content="""# Менің алғашқы постым

Бұл менің **алғашқы** постым. Мен веб-даму туралы жазамын.

## Не істеп жүрмін?

- React үйреніп жүрмін
- Next.js қолданып жүрмін
- FastAPI бэкенд жасап жүрмін

### Код мысалы:

```javascript
function hello() {
    console.log("Сәлем, әлем!");
}
```

> Бұл цитата бөлімі. Ол маңызды ақпаратты көрсетеді.

Жаңа посттар келетін болады!""",
        content_html=""
    ),
    PostFull(
        slug="fastapi-and-nextjs",
        title="FastAPI + Next.js = ❤️",
        author="Мейірхан Ахметов",
        date="2024-01-20",
        category="Даму",
        content="""# FastAPI + Next.js = ❤️

FastAPI мен Next.js комбинациясы - бұл **керемет** стек!

## Неге бұл комбинация жақсы?

1. **FastAPI** - жылдам және қарапайым бэкенд
2. **Next.js** - күшті фронтенд фреймворк
3. **TypeScript** - тип қауіпсіздігі

### API мысалы:

```python
@app.get("/api/posts")
async def get_posts():
    return {"posts": posts}
```

### Компонент мысалы:

```jsx
function PostList({ posts }) {
    return (
        <div>
            {posts.map(post => (
                <PostCard key={post.id} post={post} />
            ))}
        </div>
    );
}
```

> **Кеңес:** Бұл стекпен жұмыс істеуге кірісіңіз!

Жаңа технологиялар үйрену әрқашан қызық!""",
        content_html=""
    ),
    PostFull(
        slug="why-i-love-python",
        title="Неге мен Python-ды ұнатамын",
        author="Сара Нұрланова",
        date="2024-01-25",
        category="Программалау",
        content="""# Неге мен Python-ды ұнатамын

Python - бұл менің **сүйікті** бағдарламалау тілім!

## Python-ның артықшылықтары:

### 1. Қарапайым синтаксис
```python
def hello_world():
    print("Сәлем, әлем!")
```

### 2. Көптеген кітапханалар
- **Django** - веб-фреймворк
- **Pandas** - деректерді талдау
- **Matplotlib** - графиктер

### 3. Қауымдастық
Python қауымдастығы өте **қолдаушы** және үлкен.

## Менің жобаларым:

- [x] Блог платформасы
- [x] API сервері
- [ ] Машиндық оқыту моделі

> Python - бұл бастаушылар үшін тамаша тіл!

Келесі постта мен Django туралы жазамын.""",
        content_html=""
    ),
    PostFull(
        slug="web-development-tips",
        title="Веб-даму кеңестері",
        author="Данияр Баймағамбетов",
        date="2024-02-01",
        category="Кеңестер",
        content="""# Веб-даму кеңестері

Бұл постта мен веб-дамудағы **маңызды** кеңестерді бөлісемін.

## 1. Код жазу кеңестері

### Қателерден сақтану:
```javascript
// Жаман
if (user != null && user.name != null) {
    console.log(user.name);
}

// Жақсы
console.log(user?.name);
```

### CSS кеңестері:
```css
/* Responsive дизайн */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

@media (max-width: 768px) {
    .container {
        padding: 0 10px;
    }
}
```

## 2. Қауіпсіздік

- ✅ Парольдерді хэштеу
- ✅ SQL инъекцияларынан сақтану
- ✅ XSS шабуылдарынан қорғану

## 3. Өнімділік

> **Еске сақтаңыз:** Жылдам сайт = Бақытты пайдаланушы

### Кеңестер:
1. Кескіндерді сығу
2. CDN қолдану
3. Кэштеу

Жаңа кеңестер келетін болады!""",
        content_html=""
    )
]

# Convert markdown content to HTML for all posts
for post in fake_posts_db:
    post.content_html = markdown.markdown(post.content, extensions=['fenced_code', 'tables', 'codehilite'])

# --- API Endpoints ---

@app.get("/api/posts", response_model=List[PostBase])
async def get_all_posts():
    """Барлық посттарды қайтарады"""
    return fake_posts_db

@app.get("/api/posts/{slug}", response_model=PostFull)
async def get_post_by_slug(slug: str):
    """Берілген slug бойынша постты қайтарады"""
    for post in fake_posts_db:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/api/categories")
async def get_categories():
    """Барлық санаттарды қайтарады"""
    categories = list(set(post.category for post in fake_posts_db))
    return {"categories": categories}

@app.get("/api/posts/category/{category}")
async def get_posts_by_category(category: str):
    """Берілген санаттағы посттарды қайтарады"""
    filtered_posts = [post for post in fake_posts_db if post.category == category]
    return filtered_posts

@app.get("/")
async def root():
    return {"message": "Blog API is running"}
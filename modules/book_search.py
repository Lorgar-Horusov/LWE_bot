from interactions import Extension
from interactions import slash_command, SlashContext, slash_option
from util.flibusta_API import search_books
from load_modules import load_config


class Search(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command(
        description="Search for books on flibusta.site"
    )
    @slash_option(
        name="book_name",
        description="Title of the book to be searched",
        required=True,
        opt_type=3
    )
    @slash_option(
        name="count",
        description="Number of results to return ",
        required=False,
        opt_type=4
    )
    async def fb_search(self, ctx: SlashContext, book_name: str, count: int = None):
        config = load_config()
        if config['book_search']['enabled']:
            if count is None:
                count = config['book_search']['default_search_count']
        else:
            return await ctx.send("This command is currently disabled.", ephemeral=True)

        await ctx.defer()
        try:
            books = search_books(book_name, count)
            if books:
                response = "\n".join([
                    (f"## {book['author']}\n"
                     f"### {book['title']}\n"
                     f"- *[Book Link]({book['book_url']})*\n"
                     f"- *[Book Read]({book['book_url']}/read)*\n"
                     f"- *[Download FB2]({book['download_url_fb2']})*\n")
                    for index, book in enumerate(books)
                ])
                await ctx.send(response)
            else:
                await ctx.send("No books found.")
        except Exception as e:
            await ctx.send(f"An error occurred while searching for books: {str(e)}")

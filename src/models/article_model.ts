import BaseModel from "./base_model.ts";

export type Article = {
  author_id: number;
  body: string;
  created_at: number;
  description: string;
  id?: number;
  slug?: string;
  title: string;
  updated_at: number;
}

export class ArticleModel extends BaseModel {

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - PROPERTIES //////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  public author_id: number;
  public body: string;
  public created_at: number;
  public description: string;
  public id: number;
  public slug: string;
  public title: string;
  public updated_at: number;

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - CONSTRCUTOR /////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  constructor(
    authorId: number,
    title: string,
    description: string,
    body: string,
    slug: string = "",
    createdAt = Date.now(),
    updatedAt = Date.now()
    id: number = -1
  ) {
    super();
    this.id = id;
    this.author_id = authorId;
    this.title = title;
    this.description = description;
    this.body = body;
    this.slug = this.id == -1
      ? this.createSlug(title)
      : slug;
    this.created_at = createdAt;
    this.updated_at = updatedAt;
  }

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - METHODS - PUBLIC ////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * Delete this model.
   *
   * @return Promise<boolean>
   */
  public async delete(): Promise<boolean> {
    let query = `DELETE FROM articles WHERE id = ?`;
    query = this.prepareQuery(
      query,
      [
        String(this.id),
      ]
    );

    try {
      const client = await BaseModel.connect();
      await client.query(query);
      client.release();
    } catch (error) {
      console.log(error);
      return false;
    }
    return true;
  }

  /**
   * Save this model.
   *
   * @return Promise<ArticleModel>
   */
  public async save(): Promise<ArticleModel> {
    // If this model already has an ID, then that means we're updating the model
    if (this.id != -1) {
      return this.update();
    }

    let query = "INSERT INTO articles "
      + "(author_id, title, description, body, slug, created_at, updated_at) "
      + "VALUES (?, ?, ?, ?, ?, to_timestamp(?), to_timestamp(?));"
    query = this.prepareQuery(
      query, [
        String(this.author_id),
        this.slug,
        this.title,
        this.description,
        this.body,
        String(this.created_at),
        String(this.updated_at)
      ]
    );

    const client = await BaseModel.connect();
    client.query(query);
    client.release();

    // @ts-ignore
    //
    // (crookse) We ignore this because getArticleBySlug() can return null if
    // the article is not found. However, in this case, it will never be null.
    return ArticleModel.getArticleBySlug(this.slug);
  }

  /**
   * Update this model.
   *
   * @return Promise<ArticleModel>
   */
  public async update(): Promise<ArticleModel> {
    let query = "UPDATE articles SET "
      + "title = ?, description = ?, body = ?, updatedAt = ? "
      + `WHERE id = '${this.id}';`;
    query = this.prepareQuery(
      query,
      [
        this.title,
        this.description,
        this.body,
        Date.now()
      ]
    );
    const client = await BaseModel.connect();
    await client.query(query);
    client.release();

    // @ts-ignore
    // (crookse) We ignore this because getUserByEmail() can return null if the
    // user is not found. However, in this case, it will never be null.
    return ArticleModel.getArticleById(this.id);
  }



  protected createSlug(title: string): string {
    return title.toLowerCase()
      .replace(/[^a-zA-Z ]/g, "")
      .replace(/\s/g, "-");
  }
}

// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { NearTextType } from 'types';
import type { NextApiRequest, NextApiResponse } from 'next';
import weaviate, { WeaviateClient, ApiKey } from 'weaviate-ts-client';


export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Object>
) {
  try {
    const { method } = req;
    let { query } = req.body;
    console.log(query)
    const weaviateClusterUrl = process.env.WEAVIATE_CLUSTER_URL?.replace("https://", "")

    switch (method) {

      case 'POST': {
        const client: WeaviateClient = weaviate.client({
          scheme: 'https',
          host: "weaviate-demo-p98auhld.weaviate.network",
          apiKey: new ApiKey("zP1vIb9s7T8n2Hdac2t81ptMlsH9A2ip4OPP"), //READONLY API Key, ensure the environment variable is an Admin key to support writing
          headers: {
            'X-Cohere-Api-Key': "6fxtraxcntZPj1irCykFr2BCemAcmX65J7LudCeJ",
          },
          
        });
        console.log("WEAVIATE_CLUSTER_URL:", process.env.WEAVIATE_CLUSTER_URL);
        console.log("WEAVIATE_API_KEY:", process.env.WEAVIATE_API_KEY);
        console.log("COHERE_API_KEY:", process.env.COHERE_API_KEY);

        let nearText: NearTextType = {
          concepts: [],
        }

        nearText.certainty = .6

        nearText.concepts = query;

        const recData = await client.graphql
          .get()
          .withClassName('Book')
          .withFields(
            'title isbn10 isbn13 categories thumbnail description num_pages average_rating published_year authors'
          )
          .withNearText(nearText)
          .withLimit(20)
          .do();

        res.status(200).json(recData);
        break;
      }
      default:
        res.status(400);
        break;
    }
  } catch (err) {
    console.error(err);
    res.status(500);
  }
}

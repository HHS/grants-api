import { ApiResponseError } from "src/errors";
import { getSession } from "src/services/auth/session";
import { handleSavedOpportunity } from "src/services/fetch/fetchers/savedOpportunityFetcher";

export const POST = async (request: Request) => {
  return await handleRequest(request, "POST");
};

export const DELETE = async (request: Request) => {
  return await handleRequest(request, "DELETE");
};

const handleRequest = async (request: Request, type: "DELETE" | "POST") => {
  const headers = request.headers;
  const opportunity_id = headers.get("opportunity_id");
  const action = type === "POST" ? "save" : "delete";

  try {
    const session = await getSession();
    if (!session || !session.token) {
      throw new Error("No active session to save opportunity");
    }
    const response = await handleSavedOpportunity(
      type,
      session.token,
      session.user_id as string,
      Number(opportunity_id),
    );
    if (!response || response.status_code !== 200) {
      throw new Error(`Error ${action} saved opportunity: ${response.message}`);
    }
    return Response.json({
      type: action,
      message: `${action} saved opportunity success`,
    });
  } catch (e) {
    const error = e as Error;
    const apiError = JSON.parse(error.message) as ApiResponseError;
    return Response.json(
      {
        message: `Error attempting to ${action} saved opportunity: ${apiError.message}`,
      },
      { status: apiError.status },
    );
  }
};

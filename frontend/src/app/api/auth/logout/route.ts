import { getSession } from "src/services/auth/session";
import { deleteSession } from "src/services/auth/sessionUtils";
import { postLogout } from "src/services/fetch/fetchers/userFetcher";

export async function POST() {
  try {
    const session = await getSession();
    if (!session || !session.token) {
      throw new Error("No active session to logout");
    }
    // logout on API via /v1/users/token/logout
    const response = await postLogout(session.token);
    if (!response) {
      throw new Error("No logout response from API");
    }
    // delete session from current cookies
    await deleteSession();
    return Response.json({ message: "logout success" });
  } catch (e) {
    const { message, cause } = e as Error;
    const status = cause
      ? Object.assign(
          { status: 500 },
          JSON.parse(cause as string) as { status: number },
        ).status
      : 500;
    return Response.json(
      { message: `Error logging out: ${(cause as string) ?? message}` },
      { status },
    );
  }
}

import { useSelector, useDispatch } from "react-redux";
import { login, updateAccess, updateRefresh, logout } from "../global-state/features/authSlice";

export const useAuthTokens = () => {
  const { username, userId, accessToken, refreshToken } = useSelector((state) => state.auth);
  const dispatch = useDispatch();

  const setTokensAndUser = (userId, username, access, refresh) => {
    dispatch(login({ userId, username, access, refresh }));
  };

  const setAccess = (access) => {
    dispatch(updateAccess({ access }));
  };

  const setRefresh = (refresh) => {
    dispatch(updateRefresh({ refresh }));
  };

  const clearTokens = () => {
    dispatch(logout());
  };

  return {
    username,
    userId,
    accessToken,
    refreshToken,
    setTokensAndUser,
    setAccess,
    setRefresh,
    clearTokens,
  };
};

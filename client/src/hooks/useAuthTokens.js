import { useSelector, useDispatch } from "react-redux";
import { login, updateAcess, updateRefresh, loguout } from "../global-state/features/authSlice";

export const useAuthTokens = () => {
  const { accessToken, refreshToken } = useSelector((state) => state.auth);
  const dispatch = useDispatch();

  const setTokens = (access, refresh) => {
    dispatch(login({ access, refresh }));
  };

  const setAccess = (access) => {
    dispatch(updateAcess({ access }));
  };

  const setRefresh = (refresh) => {
    dispatch(updateRefresh({ refresh }));
  };

  const clearTokens = () => {
    dispatch(loguout());
  };

  return {
    accessToken,
    refreshToken,
    setTokens,
    setAccess,
    setRefresh,
    clearTokens,
  };
};

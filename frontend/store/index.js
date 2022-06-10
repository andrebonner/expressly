export const state = () => ({
  user: null,
  token: null,
  error: null,
  loading: false,
});

export const getter = {
  user: (state) => state.user,
  token: (state) => state.token,
  error: (state) => state.error,
  loading: (state) => state.loading,
};

export const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  setToken(state, token) {
    state.token = token;
  },
  setError(state, error) {
    state.error = error;
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
};

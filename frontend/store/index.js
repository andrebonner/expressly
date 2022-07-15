export const state = () => ({
  areas: [],
  institutions: [],
  items: [],
  cart: {
    items: [],
    total: 0,
  },
  user: null,
  token: null,
  error: null,
  loading: false,
});

export const getter = {
  areas: (state) => state.areas,
  institutions: (state) => state.institutions,
  items: (state) => state.items,
  cart: (state) => state.cart,
  user: (state) => state.user,
  token: (state) => state.token,
  error: (state) => state.error,
  loading: (state) => state.loading,
};

export const mutations = {
  setAreas(state, areas) {
    state.areas = areas;
  },
  setInstitutions(state, institutions) {
    state.institutions = institutions;
  },
  setItems(state, items) {
    state.items = items;
  },
  setCart(state, cart) {
    state.cart = cart;
  },
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

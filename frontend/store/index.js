export const state = () => ({
  areas: [],
  institutions: [],
  items: [],
  cart: {
    items: [],
    total: 0,
  },
  loading: false,
});

export const getter = {
  areas: (state) => state.areas,
  institutions: (state) => state.institutions,
  items: (state) => state.items,
  cart: (state) => state.cart,
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
  setLoading(state, loading) {
    state.loading = loading;
  },
};

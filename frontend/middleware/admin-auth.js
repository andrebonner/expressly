export default function ({ store, redirect }) {
  if (store.state.auth.loggedIn) {
    if (!store.state.auth.user?.is_admin) {
      return redirect("/");
    }
  } else {
    return redirect("/login");
  }
}

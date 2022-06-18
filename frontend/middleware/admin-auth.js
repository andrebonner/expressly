export default function ({ store, redirect }) {
  if (!store.state.auth.user?.is_admin) {
    return redirect("/login");
  }
}

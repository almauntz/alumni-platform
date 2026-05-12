<template>
  <nav>
    <div class="nav-inner">
      <router-link to="/" class="nav-link">Registracija</router-link>
      <router-link to="/admin" class="nav-link">Admin</router-link>
    </div>
  </nav>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
nav {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 1.5rem;
}

.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  gap: 1.5rem;
  height: 48px;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--text);
  border-bottom-color: var(--text);
}

main {
  flex: 1;
  padding: 2rem 1.5rem;
}
</style>

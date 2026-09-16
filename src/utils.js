export function get_src_url (path) {
    return new URL(path, import.meta.url).href;
}

export function parseJSONScript(id) {
    return JSON.parse(document.getElementById(id).textContent);
}

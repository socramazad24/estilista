export function getResults<T>(data: any): T[] {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.results)) return data.results;
  if (data && Array.isArray(data.sales)) return data.sales;
  return [];
}

export function safeText(value: unknown) {
  if (value === null || value === undefined || value === '') return '—';
  return String(value);
}

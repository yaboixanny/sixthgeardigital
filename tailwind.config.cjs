module.exports = {
  content: ['./index.html'],
  theme: {extend: {
    colors: {brand: {charcoal:'#0F172A',midnight:'#020617',card:'#1E293B',orange:'#EA580C',amber:'#F97316',lightOrange:'#FFF7ED',surface:'#F8FAFC',muted:'#64748B',border:'#E2E8F0'}},
    fontFamily: {sans:['Inter','Arial','sans-serif'],body:['Inter','Arial','sans-serif']}
  }},
  plugins: [require('@tailwindcss/forms')]
};

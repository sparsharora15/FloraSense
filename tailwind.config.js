/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/*"],
    theme: {
        extend: {
            dropShadow: {
                '3xl-g': '0 0px 20px #01c496',
                'mid-g': [
                    '0 1px 2px #01c496',
                    '0 1px 1px #01c496'
                ],
            }

        }
    },
    plugins: [],
}
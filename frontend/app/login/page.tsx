// // 'use client';

// // import { useState } from 'react';
// // import { useRouter } from 'next/navigation';
// // import apiClient from '../../lib/api-client';

// // export default function LoginPage() {
// //   const [email, setEmail] = useState('');
// //   const [password, setPassword] = useState('');
// //   const [error, setError] = useState('');
// //   const router = useRouter();

// //   const handleLogin = async (e: React.FormEvent) => {
// //     e.preventDefault();

// //     // Debug logging to see what we're sending
// //     console.log("Attempting login with:", { email: email.trim(), password: password.trim() });

// //     try {
// //       // Prepare form data to match backend expectations
// //       const formData = new URLSearchParams({
// //         email: email.trim(),
// //         password: password.trim()
// //       });

// //       const response = await apiClient.post('/auth/login', formData.toString(), {
// //         headers: {
// //           'Content-Type': 'application/x-www-form-urlencoded',
// //         }
// //       });

// //       console.log("Login successful:", response.data);

// //       // Save token to localStorage
// //       localStorage.setItem('access_token', response.data.access_token);

// //       // Redirect to tasks page
// //       router.push('/tasks');
// //     } catch (err: any) {
// //       console.error("Login error:", err);

// //       let errorText = "Login failed. Please try again.";
// //       if (err.response?.data?.detail) {
// //         const detail = err.response.data.detail;
// //         errorText = Array.isArray(detail)
// //           ? detail.map((d: any) => d.msg || d.type || "Validation error").join(", ")
// //           : detail;
// //       } else if (err.message) {
// //         errorText = err.message;
// //       }

// //       setError(errorText);
// //     }
// //   };

// //   return (
// //     <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
// //       <div className="max-w-md w-full space-y-8">
// //         <div>
// //           <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
// //             Sign in to your account
// //           </h2>
// //         </div>
// //         <form className="mt-8 space-y-6" onSubmit={handleLogin}>
// //           {error && (
// //             <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
// //               {error}
// //             </div>
// //           )}

// //           <div className="rounded-md shadow-sm -space-y-px">
// //             <div>
// //               <label htmlFor="email-address" className="sr-only">
// //                 Email address
// //               </label>
// //               <input
// //                 id="email-address"
// //                 name="email"
// //                 type="email"
// //                 autoComplete="email"
// //                 required
// //                 value={email}
// //                 onChange={(e) => setEmail(e.target.value)}
// //                 className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white dark:bg-gray-800 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
// //                 placeholder="Email address"
// //               />
// //             </div>
// //             <div>
// //               <label htmlFor="password" className="sr-only">
// //                 Password
// //               </label>
// //               <input
// //                 id="password"
// //                 name="password"
// //                 type="password"
// //                 autoComplete="current-password"
// //                 required
// //                 value={password}
// //                 onChange={(e) => setPassword(e.target.value)}
// //                 className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white dark:bg-gray-800 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
// //                 placeholder="Password"
// //               />
// //             </div>
// //           </div>

// //           <div className="flex items-center justify-between">
// //             <div className="text-sm">
// //               <a href="/register" className="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
// //                 Don't have an account? Register
// //               </a>
// //             </div>
// //           </div>

// //           <div>
// //             <button
// //               type="submit"
// //               className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
// //             >
// //               Sign in
// //             </button>
// //           </div>
// //         </form>
// //       </div>
// //     </div>
// //   );
// // }
// 'use client';

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import apiClient from "../../lib/api-client";

// export default function LoginPage() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const router = useRouter();

//   const handleLogin = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setError("");

//     try {
//       const response = await apiClient.post("/auth/login", {
//         email: email.trim(),
//         password: password.trim(),
//       });

//       localStorage.setItem("access_token", response.data.access_token);
//       router.push("/tasks");
//     } catch (err: any) {
//       console.error(err);
//       const detail = err.response?.data?.detail;
//       setError(
//         detail ? (Array.isArray(detail) ? detail.join(", ") : detail) : "Login failed"
//       );
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
//       <div className="max-w-md w-full space-y-8">
//         <h2 className="text-center text-3xl font-extrabold text-gray-900 dark:text-white">
//           Login
//         </h2>
//         {error && <div className="text-red-600">{error}</div>}
//         <form className="mt-8 space-y-6" onSubmit={handleLogin}>
//           <input
//             type="email"
//             placeholder="Email"
//             value={email}
//             required
//             onChange={(e) => setEmail(e.target.value)}
//             className="input-field"
//           />
//           <input
//             type="password"
//             placeholder="Password"
//             value={password}
//             required
//             onChange={(e) => setPassword(e.target.value)}
//             className="input-field"
//           />
//           <button
//             type="submit"
//             className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
//           >
//             Login
//           </button>
//         </form>
//       </div>
//     </div>
//   );
// }
'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import apiClient from "../../lib/api-client";
import { setToken } from "../../lib/tokenUtils";
import toast from 'react-hot-toast';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // Prepare form data to match backend expectations (form-data)
      const formData = new FormData();
      formData.append('email', email.trim());
      formData.append('password', password.trim());

      const response = await apiClient.post("/auth/login", formData);

      // Save token using utility function - backend returns access_token in response
      if (response.data.access_token) {
        setToken(response.data.access_token);
        toast.success('Login successful!');
      } else if (response.data.token) {
        // Alternative token field name
        setToken(response.data.token);
        toast.success('Login successful!');
      }

      // Redirect to Phase 2 dashboard
      router.push("/tasks");
    } catch (err: any) {
      console.error(err);
      let errorMessage = "Login failed";
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
      toast.error(errorMessage);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500 mb-2">
            TODO EVOLUTION
          </h1>
          <h2 className="text-xl font-bold text-white">
            Sign in to your account
          </h2>
        </div>
        {error && <div className="text-red-500 text-center">{error}</div>}
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="space-y-4">
            <div>
              <input
                type="email"
                placeholder="Email address"
                value={email}
                required
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                value={password}
                required
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300"
          >
            Login
          </button>
        </form>
        <div className="text-center text-sm text-gray-400 mt-4">
          Don't have an account?{' '}
          <Link href="/register" className="font-medium text-blue-400 hover:text-blue-300 transition-colors">
            Register
          </Link>
        </div>
        <div className="text-center text-sm text-gray-500 mt-6">
          <Link href="/" className="font-medium text-gray-400 hover:text-gray-300 transition-colors">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}

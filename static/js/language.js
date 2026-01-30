// Global Language Support System
// Manages multi-language functionality across the application

const AppLanguage = {
    current: 'en',
    
    translations: {
        en: {
            // Navigation
            home: 'Home',
            about: 'About',
            services: 'Services',
            department: 'Department',
            news: 'News',
            blog: 'Blog',
            contact: 'Contact',
            login: 'Login',
            signUp: 'Sign Up',
            logout: 'Logout',
            myProfile: 'My Profile',
            settings: 'Settings',
            
            // Common Buttons & Actions
            save: 'Save',
            saveChanges: 'Save Changes',
            cancel: 'Cancel',
            close: 'Close',
            submit: 'Submit',
            delete: 'Delete',
            edit: 'Edit',
            search: 'Search',
            loading: 'Loading...',
            updating: 'Updating...',
            change: 'Change',
            viewMore: 'View More',
            learnMore: 'Learn More',
            getStarted: 'Get Started',
            bookAppointment: 'Book Appointment',
            discoverMore: 'Discover More',
            startScreening: 'Start Screening',
            tryNow: 'Try Now',
            refresh: 'Refresh',
            confirm: 'Confirm',
            confirmBooking: 'Confirm Booking',
            or: 'or',
            
            // Status & Feedback
            error: 'Error',
            success: 'Success',
            warning: 'Warning',
            info: 'Information',
            guest: 'Guest',
            doctorView: 'Doctor View',
            patientView: 'Patient View',
            month: 'month',
            week: 'week',
            verified: 'Verified',
            helpful: 'Helpful',
            pending: 'Pending',
            confirmed: 'Confirmed',
            
            // Profile & Settings
            fullName: 'Full Name',
            emailAddress: 'Email Address',
            password: 'Password',
            currentPassword: 'Current Password',
            newPassword: 'New Password',
            confirmPassword: 'Confirm New Password',
            changePassword: 'Change Password',
            updatePassword: 'Update Password',
            enterCurrentPassword: 'Enter current password',
            enterNewPassword: 'Enter new password',
            confirmNewPassword: 'Confirm new password',
            emailCannotChange: 'Email cannot be changed securely.',
            changeYourPassword: 'Change your account password',
            lastChanged: 'Last changed',
            managePersonalInfo: 'Manage your personal information',
            
            // Settings Page
            general: 'General',
            security: 'Security',
            patientManagement: 'Patient Management',
            generalPreferences: 'General Preferences',
            securitySettings: 'Security Settings',
            languageRegion: 'Language & Region',
            preferredLanguage: 'Preferred Language',
            selectLanguage: 'Select your preferred language for the interface',
            reportSettings: 'Report Settings',
            autoSaveReports: 'Auto-save Reports',
            autoSaveDesc: 'Automatically save analysis reports to your account',
            notifications: 'Notifications',
            emailNotifications: 'Email Notifications',
            emailNotifDesc: 'Receive updates about appointments',
            passwordChangeInfo: 'Password changes require re-authentication.',
            patientRecords: 'Patient Records',
            managePatients: 'Manage registered patients and their accounts.',
            searchPatients: 'Search patients by name or email...',
            loadingRecords: 'Loading records...',
            id: 'ID',
            patient: 'Patient',
            email: 'Email',
            status: 'Status',
            actions: 'Actions',
            
            // Home Page Hero - New Design
            trustedBy: 'Trusted by 10,000+ Healthcare Professionals',
            heroLine1: 'Next-Gen',
            heroLine2: 'Oral Health AI',
            heroLine3: 'Platform',
            welcomeTitle: 'AI-Powered Appointment & Disease Detection',
            welcomeSubtitle: 'Seamlessly manage patient appointments and perform professional grade analysis for early detection of oral cancer using state-of-the-art AI.',
            advancedOralHealth: 'Advanced Oral Health',
            schedule: 'Schedule',
            viewCalendar: 'View Calendar',
            accuracyRate: 'Accuracy Rate',
            analysisTime: 'Analysis Time',
            compliant: 'Compliant',
            accuracy: 'Accuracy',
            results: 'Results',
            secure: 'Secure',
            readyToScan: 'Ready to Scan',
            detection: 'Detection',
            speed: 'Speed',
            aiModels: 'AI Models',
            noIssues: 'No Issues',
            detected: 'Detected',
            aiPowered: 'AI Powered',
            analysis: 'Analysis',
            scrollToExplore: 'Scroll to explore',
            
            // Quick Actions - New Design
            quickAccess: 'QUICK ACCESS',
            whatToDo: 'What would you like to do?',
            aiScreening: 'AI Screening',
            analyzeImages: 'Analyze oral images with AI',
            scheduleVisit: 'Schedule your next visit',
            manageSchedule: 'Manage your schedule',
            getHelp: 'Get Help',
            talkToExpert: 'Talk to an expert',
            aiAnalysis: 'AI Analysis',
            scheduleMeeting: 'Schedule Meeting',
            viewReports: 'View Reports',
            analysisHistory: 'Analysis History',
            contactDoctor: 'Contact Doctor',
            getSupport: 'Get Support',
            
            // Calendar Section
            appointmentCalendar: 'Appointment Calendar',
            calendarDesc: 'View and manage your appointments. Click on any date to see details or book a new appointment.',
            loginToViewAppointments: 'Login to view your appointments',
            upcomingAppointments: 'Upcoming Appointments',
            legend: 'Legend',
            colorGuide: 'Color Guide',
            patientAppointments: 'Patient Appointments',
            
            // Calendar & Booking
            dailySchedule: 'Daily Schedule',
            selectDate: 'Select a date',
            noAppointments: 'No appointments scheduled',
            enjoyFreeTime: 'Enjoy your free time, Doctor.',
            doctor: 'Doctor',
            time: 'Time',
            dateTime: 'Date & Time',
            notes: 'Notes',
            noNotesProvided: 'No notes provided',
            yourAppointments: 'Your Appointments',
            editAppointment: 'Edit Appointment',
            saveChanges: 'Save Changes',
            
            // Guest Access Modal
            welcome: 'Welcome!',
            needAccountToManage: 'You need an account to manage appointments.',
            logIn: 'Log In',
            createAccount: 'Create Account',
            
            // Why Choose Section
            whyChooseTitle: 'Why Choose Oral AI?',
            whyChooseHeading: 'Bridging Medical Expertise with Artificial Intelligence',
            whyChooseDesc: 'We empower dental professionals with second-opinion AI tools that detect abnormalities faster and more accurately than ever before.',
            instantResults: 'Instant Results',
            instantResultsDesc: 'Real-time analysis',
            highPrecision: 'High Precision',
            highPrecisionDesc: 'Microscopic detail',
            secureData: 'Secure Data',
            secureDataDesc: 'HIPAA Compliant',
            expertSupport: 'Expert Support',
            expertSupportDesc: 'Verified by doctors',
            
            // Services Section
            ourServices: 'OUR SERVICES',
            comprehensiveAnalysis: 'Comprehensive AI Analysis',
            comprehensiveAnalysisDesc: 'Our multi-model architecture ensures every case is handled by a specialist algorithm designed for that specific modality.',
            smartTriage: 'Smart Triage',
            smartTriageDesc: 'Intelligent routing system that automatically classifies uploaded images and directs them to the appropriate diagnostic model.',
            tryTriage: 'Try Triage',
            histopathology: 'Histopathology',
            histopathologyDesc: 'Microscopic analysis for precise tumour grading, invasion depth measurement, and perineural invasion detection.',
            analyzeSlide: 'Analyze Slide',
            clinicalScreening: 'Clinical Screening',
            clinicalScreeningDesc: 'Real-time object detection for identifying lesions, caries, and other visible oral health concerns from standard photos.',
            
            // CTA Section
            trustedHealthcare: 'TRUSTED HEALTHCARE',
            empoweringDetection: 'Empowering Early Detection Saving Lives.',
            empoweringDesc: 'Join thousands of patients and clinicians who trust Oral AI for rapid, accurate, and accessible oral health screening.',
            accuracyRate: 'Accuracy Rate',
            patientsScreened: 'Patients Screened',
            aiAvailability: 'AI Availability',
            needExpertAdvice: 'Need Expert Advice?',
            expertAdviceDesc: 'Our medical team is here to help interpret your results and guide your next steps.',
            callUsNow: 'Call Us Now',
            emailSupport: 'Email Support',
            
            // Testimonials
            testimonials: 'TESTIMONIALS',
            whatPatientsSay: 'What Our Patients Say',
            realStories: 'Real stories from people who have used our AI screening tool for early detection and peace of mind.',
            patient: 'Patient',
            regularUser: 'Regular User',
            dentalHygienist: 'Dental Hygienist',
            
            // Footer
            footerTagline: 'Pioneering the future of dental diagnostics with advanced AI technology. Accurate, fast, and accessible healthcare for everyone.',
            platform: 'Platform',
            aboutUs: 'About Us',
            ourTeams: 'Our Teams',
            tryAITool: 'Try AI Tool',
            legal: 'Legal',
            privacyPolicy: 'Privacy Policy',
            termsOfService: 'Terms of Service',
            cookiePolicy: 'Cookie Policy',
            hipaaCompliance: 'HIPAA Compliance',
            stayUpdated: 'Stay Updated',
            newsletterDesc: 'Subscribe to our newsletter for the latest AI medical breakthroughs.',
            enterYourEmail: 'Enter your email',
            join: 'Join',
            allRightsReserved: 'All rights reserved',
            designedForHealthcare: 'Designed for better healthcare.',
            
            // Login Page
            signIn: 'Sign In',
            signInTitle: 'Sign In',
            enterCredentials: 'Enter your credentials to access your account',
            rememberMe: 'Remember me',
            forgotPassword: 'Forgot password?',
            signingIn: 'Signing In...',
            dontHaveAccount: "Don't have an account?",
            welcomeBack: 'Welcome Back.',
            loginDesc: 'Access your personalized dashboard to manage appointments, view analysis reports, and connect with medical professionals seamlessly.',
            accuracyRate: 'Accuracy Rate',
            aiAvailability: 'AI Availability',
            
            // Register Page
            joinUsToday: 'Join Us Today.',
            registerDesc: 'Create an account to access state-of-the-art AI oral screening, manage appointments with specialists, and track your oral health journey.',
            freeInitialScreening: 'Free Initial AI Screening',
            secureMedicalRecords: 'Secure Medical Records',
            directSpecialistBooking: 'Direct Specialist Booking',
            fillDetails: 'Fill in your details to get started',
            iAmA: 'I am a...',
            patientRole: 'Patient (I want to check my health)',
            doctorRole: 'Medical Professional (I want to treat)',
            creatingAccount: 'Creating Account...',
            alreadyHaveAccount: 'Already have an account?',
            bySigningUp: 'By signing up, you agree to our',
            terms: 'Terms',
            and: '&',
            
            // About Page
            whoWeAre: 'Who We Are',
            aboutOralAI: 'About Oral AI',
            aboutDesc: 'Pioneering the future of dental diagnostics through the convergence of medical expertise and advanced artificial intelligence.',
            ourMission: 'Our Mission',
            democratizingHealthcare: 'Democratizing Advanced Oral Healthcare',
            missionDesc: 'Our mission is to make high-quality oral disease detection accessible to everyone. By leveraging cutting-edge AI technology, we provide dental professionals with powerful tools to identify potential issues early, leading to better patient outcomes and saved lives.',
            analysisAccuracy: 'Analysis Accuracy',
            systemAvailability: 'System Availability',
            ourCoreValues: 'Our Core Values',
            whatDrivesUs: 'What Drives Us',
            patientFirst: 'Patient First',
            patientFirstDesc: 'Every algorithm we develop and every feature we build is designed with the ultimate goal of improving patient care and safety.',
            scientificRigor: 'Scientific Rigor',
            scientificRigorDesc: 'We adhere to the highest standards of scientific validation. Our models are rigorously tested and continuously improved.',
            dataPrivacy: 'Data Privacy',
            dataPrivacyDesc: 'We treat patient data with the utmost respect and security, complying with all major healthcare data protection regulations.',
            ourTechnology: 'Our Technology',
            poweredByInnovation: 'Powered by Innovation',
            techDesc: 'Click on the cards below to explore the cutting-edge tools behind our AI.',
            deepLearningFramework: 'Deep Learning Framework',
            explore: 'Explore',
            
            // Contact Page
            getInTouch: 'Get in Touch',
            hereToHelp: "We're Here to Help",
            contactDesc: 'Have questions about our AI technology or need support? Reach out to our team.',
            contactInformation: 'Contact Information',
            teamAvailable: 'Our team is available Monday through Friday to assist you with any inquiries.',
            emailUs: 'Email Us',
            callUs: 'Call Us',
            visitUs: 'Visit Us',
            followUs: 'Follow Us',
            sendMessage: 'Send us a Message',
            subject: 'Subject',
            message: 'Message',
            generalInquiry: 'General Inquiry',
            technicalSupport: 'Technical Support',
            partnershipOpportunity: 'Partnership Opportunity',
            pressMedia: 'Press & Media',
            howCanWeHelp: 'How can we help you?',
            supportCenter: 'Support Center',
            faq: 'Frequently Asked Questions',
            faqDesc: "Everything you need to know about Oral AI's technology and services.",
            howAccurate: 'How accurate is the AI diagnosis?',
            accuracyAnswer: 'Our dual-model system has achieved 99.9% accuracy in clinical trials. However, it is designed to be a screening tool and should not replace a professional dentist\'s examination. We recommend using it for early detection and monitoring.',
            
            // Triage/Analysis Page
            aiPoweredDiagnostics: 'AI-POWERED DIAGNOSTICS',
            intelligentAnalysis: 'Intelligent Oral Disease Analysis',
            triageDesc: 'Deploying state-of-the-art AI to classify clinical images and histopathology slides with precision. Upload your sample to begin the automated triage process.',
            dropImageHere: 'Drop your image here, or click to browse',
            supportsFormats: 'Supports JPG, JPEG, PNG (Clinical or Histopathology)',
            secureUpload: 'Secure & Private Upload',
            analyzingImage: 'Analyzing Image Structure...',
            routingToModel: 'Routing to appropriate specialist model',
            systemCapabilities: 'System Capabilities',
            smartTriage: 'Smart Triage',
            smartTriageDesc: 'Intelligent routing system that automatically classifies uploaded images and directs them to the appropriate diagnostic model.',
            autoRouting: 'Auto-Routing',
            histopathology: 'Histopathology',
            histopathologyDesc: 'Microscopic analysis for precise tumour grading, invasion depth measurement, and perineural invasion detection.',
            deepLearning: 'Deep Learning',
            clinicalScreening: 'Clinical Screening',
            clinicalScreeningDesc: 'Real-time object detection for identifying lesions, caries, and other visible oral health concerns from standard photos.',
            objectDetection: 'Object Detection',
            triageSmartDesc: 'Automatically routes uploaded images to either the Histopathology or Clinical Screening model based on visual characteristics.',
            histopathologyDeepDesc: 'Deep learning analysis for tumour detection, grading, and invasion depth measurement on microscopic slides.',
            clinicalRealTimeDesc: 'Real-time object detection for oral hygiene assessment and identification of potential lesions or abnormalities.',
            
            // Model A (Histopathology)
            histopathologyAnalysis: 'Histopathology Analysis',
            aiAnalysisInsight: 'AI Analysis Insight',
            loadingSuggestion: 'Loading suggestion...',
            primaryDiagnosis: 'Primary Diagnosis',
            analyzing: 'Analyzing...',
            confidence: 'Confidence',
            microscopicFeatures: 'Microscopic Features',
            depthOfInvasion: 'Depth of Invasion',
            original: 'Original',
            heatmap: 'Heatmap',
            heatmapInfo: 'Heatmaps visualize high-probability tumour regions. Toggle between views to compare.',
            
            // Model B (Clinical)
            clinicalAnalysis: 'Clinical Analysis',
            detectedConditions: 'Detected Conditions',
            noConditionsDetected: 'No conditions detected',
            
            // Chat Widget
            aiAssistant: 'AI Assistant',
            onlineStatus: 'Online - Ready to help',
            askAnything: 'Ask anything about oral health...',
            typeMessage: 'Type your message...',
            send: 'Send',
            clearChat: 'Clear Chat',
            
            // Messages
            passwordUpdated: 'Password updated successfully! Your account is now more secure.',
            passwordMismatch: 'New passwords do not match! Please try again.',
            passwordTooShort: 'New password must be at least 6 characters long.',
            networkError: 'Network error. Please check your connection and try again.',
            languageChanged: 'Language changed successfully. Interface updated!',
            autoSaveEnabled: 'Auto-save enabled. Your reports will be saved automatically.',
            autoSaveDisabled: 'Auto-save disabled. You will need to manually save reports.',
            emailNotifEnabled: 'Email notifications enabled. You will receive appointment updates.',
            emailNotifDisabled: 'Email notifications disabled. You will not receive appointment emails.',
            profileUpdated: 'Profile updated successfully!',
            pleaseEnterName: 'Please enter a valid name',
            appointmentBooked: 'Appointment Booked!',
            pleaseSelectTime: 'Please select a time',
            failedToBook: 'Failed to book',
            sessionExpired: 'Session Expired',
            
            // Additional Login/Register
            loginBrandingDesc: 'Access your personalized dashboard to manage appointments, view analysis reports, and connect with medical professionals seamlessly.',
            registerBrandingDesc: 'Create an account to access state-of-the-art AI oral screening, manage appointments with specialists, and track your oral health journey.',
            fillInDetails: 'Fill in your details to get started',
            rolePatient: 'Patient (I want to check my health)',
            roleDoctor: 'Medical Professional (I want to treat)',
            fullNamePlaceholder: 'John Doe',
            emailPlaceholder: 'name@example.com',
            copyrightText: '© 2026 Oral AI Platform. All rights reserved.',
            appName: 'Oral AI',
            
            // About Page Additional
            aboutHeroDesc: 'Pioneering the future of dental diagnostics through the convergence of medical expertise and advanced artificial intelligence.',
            techSectionDesc: 'Click on the cards below to explore the cutting-edge tools behind our AI.',
            gpuAcceleration: 'GPU Acceleration',
            realTimeObjectDetection: 'Real-Time Object Detection',
            beginner: 'Beginner',
            advanced: 'Advanced',
            
            // Contact Page Additional
            contactHeroDesc: 'Have questions about our AI technology or need support? Reach out to our team.',
            teamAvailability: 'Our team is available Monday through Friday to assist you with any inquiries.',
            businessHours: 'Mon-Fri, 9am - 6pm EST',
            sendUsMessage: 'Send us a Message',
            messagePlaceholder: 'How can we help you?',
            faqAccuracyQuestion: 'How accurate is the AI diagnosis?',
            faqAccuracyAnswer: 'Our dual-model system has achieved <strong>99.9% accuracy</strong> in clinical trials. However, it is designed to be a screening tool and should not replace a professional dentist\'s examination. We recommend using it for early detection and monitoring.',
            faqSecurityQuestion: 'Is my medical data secure?',
            faqSecurityAnswer: 'Yes. We are fully <strong>HIPAA compliant</strong> and use end-to-end encryption for all uploaded images and patient data. We do not store your images permanently without your explicit consent, ensuring your privacy is always protected.',
            faqApiQuestion: 'Can I integrate this API into my clinic\'s software?',
            faqApiAnswer: 'Absolutely. We offer a robust RESTful API designed for seamless integration with existing Electronic Health Record (EHR) systems. Please select "Partnership Opportunity" in the contact form above to request documentation and API keys.',
            faqTimeQuestion: 'How long does the analysis take?',
            faqTimeAnswer: 'The analysis is near-instantaneous. Our optimized inference engine typically processes high-resolution images in <strong>under 2 seconds</strong>, providing you with immediate feedback and a downloadable PDF report.',
            faqConditionsQuestion: 'What conditions can the AI detect?',
            faqConditionsAnswer: 'Currently, our model is trained to detect early signs of <strong>Gingivitis, Dental Caries (Cavities), and Periodontitis</strong>. We are actively working on expanding our dataset to include oral cancer screening and orthodontic assessments.',
            
            // Triage Page Additional
            intelligentOralAnalysis: 'Intelligent Oral Disease Analysis',
            triageSubtitle: 'Deploying state-of-the-art AI to classify clinical images and histopathology slides with precision. Upload your sample to begin the automated triage process.',
            supportsImageFormats: 'Supports JPG, JPEG, PNG (Clinical or Histopathology)',
            securePrivateUpload: 'Secure & Private Upload',
            analyzingImageStructure: 'Analyzing Image Structure...',
            smartTriageFeatureDesc: 'Automatically routes uploaded images to either the Histopathology or Clinical Screening model based on visual characteristics.',
            histopathologyFeatureDesc: 'Deep learning analysis for tumour detection, grading, and invasion depth measurement on microscopic slides.',
            clinicalScreeningFeatureDesc: 'Real-time object detection for oral hygiene assessment and identification of potential lesions or abnormalities.',
            
            // Model A Additional
            toggleFullscreen: 'Toggle Fullscreen',
            heatmapInfoNote: 'Heatmaps visualize high-probability tumour regions. Toggle between views to compare.',
            patternOfInvasion: 'Pattern of Invasion',
            perineuralInvasion: 'Perineural Invasion',
            mitoticIndex: 'Mitotic Index',
            tumourBudsCount: 'Tumour Buds Count',
            viewAiRecommendation: 'View AI Recommendation',
            pdfReport: 'PDF Report',
            emailReport: 'Email Report',
            startNewAnalysis: 'Start New Analysis',
            
            // Model B Additional
            lowQualityImage: 'Low Quality Image',
            detections: 'Detections',
            fullscreen: 'Fullscreen',
            screeningResult: 'Screening Result',
            hygieneScore: 'Hygiene Score',
            waitingForAnalysis: 'Waiting for analysis...',
            
            // Chat Widget Additional
            oralAiAssistant: 'Oral AI Assistant',
            onlineReady: 'Online & Ready',
            minimize: 'Minimize',
            chatWelcomeMessage: 'Hello! I\'m your AI medical assistant. I can help explain your analysis results or answer general questions about oral health.',
            justNow: 'JUST NOW',
            suggestedTopics: 'Suggested Topics',
            whatIsOralCancer: 'What is Oral Cancer?',
            explainHistopathology: 'Explain Histopathology',
            howDoesAiWork: 'How does the AI work?',
            chatInputPlaceholder: 'Type your question...',
            aiDisclaimer: 'AI can make mistakes. Verify important info.',
            
            // Department Page
            ourExperts: 'Our Experts',
            meetTheTeam: 'Meet The Team',
            departmentHeroDesc: 'The brilliant minds behind Oral AI, dedicated to revolutionizing dental diagnostics through collaboration and innovation.',
            systems: 'SYSTEMS',
            backendDesign: 'Backend Design',
            backendDeveloper: 'Backend Developer',
            backendDevDesc: 'Architecting robust APIs and managing high-performance model inference engines.',
            uiux: 'UI/UX',
            frontendDesign: 'Frontend Design',
            frontendDeveloper: 'Frontend Developer',
            frontendDevDesc: 'Crafting intuitive and responsive user interfaces for seamless medical analysis.',
            dataTeam: 'DATA TEAM',
            datasetAnnotation: 'Dataset Annotation & Preparation',
            datasetAnnotationDesc: 'Ensuring the highest quality data for training our AI models.',
            datasetSpecialist: 'Dataset Specialist',
            datasetSpecialistDesc1: 'Expert in medical image annotation and data preprocessing pipelines.',
            datasetSpecialistDesc2: 'Specializes in data quality assurance and dataset balancing techniques.',
            datasetSpecialistDesc3: 'Focuses on pathological feature extraction and metadata management.',
            
            // Blog Page
            oralAiJournal: 'The Oral AI Journal',
            blogHeroTitle: 'Insights, Updates & Stories',
            blogHeroDesc: 'Deep dives into our technology, patient health guides, and the future of AI in dentistry.',
            engineering: 'Engineering',
            featuredPostTitle: 'The Architecture of Accuracy: Inside Oral AI\'s Dual-Model System',
            featuredPostDesc: 'How we combined a Triage Router with specialized Clinical and Histopathological models to achieve 99.8% diagnostic precision.',
            readArticle: 'Read Article',
            ourBlog: 'Our Blog',
            latestArticles: 'Latest Articles',
            patientHealth: 'Patient Health',
            blogPost1Title: '5 Early Signs of Oral Health Issues You Shouldn\'t Ignore',
            blogPost1Desc: 'From subtle discoloration to minor sensitivity, learn what your mouth is trying to tell you before it becomes a major problem.',
            behindTheScenes: 'Behind the Scenes',
            blogPost2Title: 'From Data to Diagnosis: How We Built Our Dataset',
            blogPost2Desc: 'A look at the rigorous curation process our Dataset Team uses to ensure our AI learns from the highest quality medical imagery.',
            futureTech: 'Future Tech',
            blogPost3Title: 'The Future of Tele-Dentistry: AI as a First Responder',
            blogPost3Desc: 'Imagine getting a preliminary diagnosis from your smartphone. Here\'s how Oral AI is making remote screening a reality.',
            
            // News/Pages Page
            industryInsights: 'Industry Insights',
            eraOfMedicalAi: 'The Era of Medical AI',
            pagesHeroDesc: 'Discover how Artificial Intelligence is reshaping the landscape of healthcare, from early diagnosis to personalized treatment plans.',
            diagnostics: 'Diagnostics',
            newsArticle1Title: 'AI Outperforms Human Experts in Early Cancer Detection',
            newsArticle1Desc: 'Recent studies show deep learning models achieving 99% accuracy in identifying early-stage anomalies in medical imaging, significantly reducing false negatives.',
            readFullStory: 'Read Full Story',
            robotics: 'Robotics',
            newsArticle2Title: 'Precision Surgery: The Rise of AI-Assisted Operations',
            newsArticle2Desc: 'Surgeons are now leveraging AI-powered robotic arms to perform complex procedures with sub-millimeter precision, minimizing recovery time for patients.',
            pharma: 'Pharma',
            newsArticle3Title: 'Accelerating Drug Discovery',
            newsArticle3Desc: 'Generative AI is slashing drug development timelines from years to months by predicting molecular interactions.',
            genomics: 'Genomics',
            newsArticle4Title: 'Hyper-Personalized Medicine',
            newsArticle4Desc: 'AI algorithms analyzing genomic data can now tailor treatment plans specifically to an individual\'s DNA profile.',
            patientCare: 'Patient Care',
            newsArticle5Title: '24/7 Virtual Health Assistants',
            newsArticle5Desc: 'LLM-powered chatbots are providing instant, accurate medical triage and mental health support globally.',
            joinTheRevolution: 'Join the Revolution',
            joinRevolutionDesc: 'Oral AI is at the forefront of this transformation. Experience our cutting-edge diagnostic tools today.',
            tryOralAiNow: 'Try Oral AI Now',
            
            // CTA Section
            trustedHealthcare: 'TRUSTED HEALTHCARE',
            empoweringEarlyDetection: 'Empowering Early Detection<br>Saving Lives.',
            joinThousandsDesc: 'Join thousands of patients and clinicians who trust Oral AI for rapid, accurate, and accessible oral health screening.',
            accuracyRate: 'Accuracy Rate',
            patientsScreened: 'Patients Screened',
            aiAvailability: 'AI Availability',
            supportLabel: 'SUPPORT',
            needExpertAdvice: 'Need Expert Advice?',
            medicalTeamHelp: 'Our medical team is here to help interpret your results and guide your next steps.',
            callUsNow: 'Call Us Now',
            emailSupport: 'Email Support',
            
            // Testimonials
            testimonialsLabel: 'TESTIMONIALS',
            whatPatientsSay: 'What Our Patients Say',
            testimonialsDesc: 'Real stories from people who have used our AI screening tool for early detection and peace of mind.',
            testimonial1: '"The AI screening was incredibly fast. I was worried about a spot on my gum, and the tool gave me an immediate assessment that helped me decide to see a doctor."',
            testimonial2: '"As a smoker, I worry about oral health. This app helps me keep track of changes. The report generation is very professional and easy to understand."',
            testimonial3: '"I recommend this to my patients for self-monitoring between visits. The accuracy of the lesion detection is impressive and reliable."',
            testimonial4: '"The interface is so easy to use. I just uploaded a photo and got results in seconds. It gave me peace of mind when I needed it most."',
            testimonial5: '"Great tool for educational purposes too. It helps visualize what different oral conditions look like. Very helpful for students."',
            testimonial6: '"I had a concern about a sore that wasn\'t healing. The app suggested I see a specialist, and I\'m glad I did. Early detection works."',
            rolePatient: 'Patient',
            roleRegularUser: 'Regular User',
            roleDentalHygienist: 'Dental Hygienist',
            roleStudent: 'Student',
            roleDoctor: 'Doctor',
            roleAdmin: 'Admin',
            
            // Notifications
            notificationsTitle: 'Notifications',
            markAllRead: 'Mark all read',
            noNewNotifications: 'No new notifications',
            allCaughtUp: 'All Caught Up!',
            noNewNotificationsOrAppointments: 'No new notifications or appointments.',
            
            // Model B Results
            qualityNoteLowRes: 'Low Resolution. Switched to Standard Mode for better stability.',
            screeningResultNormal: 'Normal',
            screeningResultRefertoDentist: 'Refer to Dentist',
            hygieneScoreHigh: 'High',
            hygieneScoreMedium: 'Medium',
            hygieneScoreLow: 'Low',
            noIssuesDetected: 'No specific issues detected.',
            detectedCount: '{count} detected',
            conditionCaries: 'Caries',
            conditionGingivitis: 'Gingivitis',
            conditionUlcer: 'Ulcer',
            conditionTooth: 'Tooth',
            conditionCalculus: 'Calculus',
            conditionHypodontia: 'Hypodontia',
            
            // Model A Results
            tumourDetected: 'Tumour Detected',
            noTumour: 'No Tumour',
            detected: 'Detected',
            notDetected: 'Not Detected',
            
            // Technology Modal
            techPytorchSubtitle: 'Deep Learning Framework',
            techPytorchBeginner: "PyTorch, developed by Facebook, is another deep learning framework widely used for building neural networks. Its straightforward, Pythonic nature makes it easy for beginners to grasp the basics of model creation and training. Beginners will appreciate PyTorch's flexibility in creating simple models for image classification without having to worry about too much technical overhead.",
            techPytorchAdvanced: "Advanced users can use PyTorch's dynamic computation graph, allowing greater flexibility when building complex architectures, custom loss functions, and optimizers. It's a great choice for researchers, as PyTorch offers seamless experimentation with cutting-edge models like Vision Language Models, Generative Adversarial Networks (GANs) and deep reinforcement learning. Thanks to its efficient memory management and GPU support, it also excels in handling large datasets.",
            techCudaSubtitle: 'GPU Acceleration',
            techCudaBeginner: "CUDA is a parallel computing platform and programming model developed by NVIDIA, while cuDNN is a GPU-accelerated library for deep neural networks. For beginners, these tools may seem technical, but their primary purpose is to accelerate the training of deep learning models by utilizing GPU power. By setting up CUDA and cuDNN properly within the training environment, a significant boost in speed and optimization of model training can be achieved, especially when working with frameworks like TensorFlow and PyTorch.",
            techCudaAdvanced: "Experts can harness the full power of CUDA and cuDNN to optimize performance in high-demand applications. This includes writing custom CUDA kernels for specific operations, managing GPU memory efficiently, and fine-tuning neural network training for maximum speed and scalability. These tools are essential for developers working with large datasets and needing top-tier performance from their models.",
            techYoloSubtitle: 'Real-Time Object Detection',
            techYoloBeginner: "YOLO (You Only Look Once) is a fast object detection algorithm that is especially popular for real-time applications. Beginners can use pre-trained YOLO models to quickly detect objects in images or videos with relatively simple code. The ease of use makes YOLO a great entry point for those looking to explore object detection without needing to build complex models from scratch.",
            techYoloAdvanced: "YOLO provides opportunities for fine-tuning models on custom datasets to detect specific objects, improving detection speed and accuracy. YOLO's lightweight nature allows it to be deployed in resource-constrained environments, like mobile devices, making it a go-to solution for real-time applications. Professionals can also experiment with newer versions of YOLO, adjusting parameters to fit specific project needs."
        },
        ms: {
            // Navigation
            home: 'Laman Utama',
            about: 'Tentang',
            services: 'Perkhidmatan',
            department: 'Jabatan',
            news: 'Berita',
            blog: 'Blog',
            contact: 'Hubungi',
            login: 'Log Masuk',
            signUp: 'Daftar',
            logout: 'Log Keluar',
            myProfile: 'Profil Saya',
            settings: 'Tetapan',
            
            // Common Buttons & Actions
            save: 'Simpan',
            saveChanges: 'Simpan Perubahan',
            cancel: 'Batal',
            close: 'Tutup',
            submit: 'Hantar',
            delete: 'Padam',
            edit: 'Edit',
            search: 'Cari',
            loading: 'Memuatkan...',
            updating: 'Mengemaskini...',
            change: 'Tukar',
            viewMore: 'Lihat Lagi',
            learnMore: 'Ketahui Lebih Lanjut',
            getStarted: 'Mulakan',
            bookAppointment: 'Tempah Temujanji',
            discoverMore: 'Ketahui Lebih Lanjut',
            startScreening: 'Mula Saringan',
            tryNow: 'Cuba Sekarang',
            refresh: 'Muat Semula',
            confirm: 'Sahkan',
            confirmBooking: 'Sahkan Tempahan',
            or: 'atau',
            
            // Status & Feedback
            error: 'Ralat',
            success: 'Berjaya',
            warning: 'Amaran',
            info: 'Maklumat',
            guest: 'Tetamu',
            doctorView: 'Paparan Doktor',
            patientView: 'Paparan Pesakit',
            month: 'bulan',
            week: 'minggu',
            verified: 'Disahkan',
            helpful: 'Membantu',
            pending: 'Menunggu',
            confirmed: 'Disahkan',
            edit: 'Edit',
            search: 'Cari',
            loading: 'Memuatkan...',
            updating: 'Mengemaskini...',
            change: 'Tukar',
            viewMore: 'Lihat Lagi',
            learnMore: 'Ketahui Lebih Lanjut',
            getStarted: 'Mulakan',
            bookAppointment: 'Tempah Temujanji',
            
            // Status & Feedback
            error: 'Ralat',
            success: 'Berjaya',
            warning: 'Amaran',
            info: 'Maklumat',
            
            // Profile & Settings
            fullName: 'Nama Penuh',
            emailAddress: 'Alamat E-mel',
            password: 'Kata Laluan',
            currentPassword: 'Kata Laluan Semasa',
            newPassword: 'Kata Laluan Baharu',
            confirmPassword: 'Sahkan Kata Laluan Baharu',
            changePassword: 'Tukar Kata Laluan',
            updatePassword: 'Kemas Kini Kata Laluan',
            enterCurrentPassword: 'Masukkan kata laluan semasa',
            enterNewPassword: 'Masukkan kata laluan baharu',
            confirmNewPassword: 'Sahkan kata laluan baharu',
            emailCannotChange: 'E-mel tidak boleh diubah dengan selamat.',
            changeYourPassword: 'Tukar kata laluan akaun anda',
            lastChanged: 'Terakhir ditukar',
            
            // Settings Page
            general: 'Umum',
            security: 'Keselamatan',
            patientManagement: 'Pengurusan Pesakit',
            generalPreferences: 'Tetapan Umum',
            securitySettings: 'Tetapan Keselamatan',
            languageRegion: 'Bahasa & Wilayah',
            preferredLanguage: 'Bahasa Pilihan',
            selectLanguage: 'Pilih bahasa pilihan anda untuk antara muka',
            reportSettings: 'Tetapan Laporan',
            autoSaveReports: 'Auto-simpan Laporan',
            autoSaveDesc: 'Simpan laporan analisis secara automatik ke akaun anda',
            notifications: 'Pemberitahuan',
            emailNotifications: 'Pemberitahuan E-mel',
            emailNotifDesc: 'Terima kemas kini tentang temujanji',
            passwordChangeInfo: 'Perubahan kata laluan memerlukan pengesahan semula.',
            
            // Home Page Hero
            welcomeTitle: 'Temujanji & Pengesanan Penyakit Berkuasa AI',
            welcomeSubtitle: 'Uruskan temujanji pesakit dengan lancar dan lakukan analisis gred profesional untuk pengesanan awal kanser mulut menggunakan AI terkini.',
            advancedOralHealth: 'Kesihatan Mulut Termaju',
            discoverMore: 'Ketahui Lebih Lanjut',
            startScreening: 'Mula Saringan',
            tryNow: 'Cuba Sekarang',
            
            // Why Choose Section
            whyChooseTitle: 'Mengapa Pilih Oral AI?',
            whyChooseHeading: 'Merapatkan Kepakaran Perubatan dengan Kecerdasan Buatan',
            whyChooseDesc: 'Kami memperkasakan profesional pergigian dengan alat AI pendapat kedua yang mengesan keabnormalan lebih cepat dan tepat berbanding sebelumnya.',
            instantResults: 'Keputusan Segera',
            instantResultsDesc: 'Analisis masa nyata',
            highPrecision: 'Ketepatan Tinggi',
            highPrecisionDesc: 'Perincian mikroskopik',
            secureData: 'Data Selamat',
            secureDataDesc: 'Pematuhan HIPAA',
            expertSupport: 'Sokongan Pakar',
            expertSupportDesc: 'Disahkan oleh doktor',
            
            // Services Section
            ourServices: 'PERKHIDMATAN KAMI',
            comprehensiveAnalysis: 'Analisis AI Komprehensif',
            comprehensiveAnalysisDesc: 'Seni bina pelbagai model kami memastikan setiap kes dikendalikan oleh algoritma pakar yang direka untuk modaliti khusus tersebut.',
            smartTriage: 'Triage Pintar',
            smartTriageDesc: 'Sistem penghalaan pintar yang secara automatik mengklasifikasikan imej yang dimuat naik dan mengarahkannya ke model diagnostik yang sesuai.',
            tryTriage: 'Cuba Triage',
            histopathology: 'Histopatologi',
            histopathologyDesc: 'Analisis mikroskopik untuk penggredan tumor yang tepat, pengukuran kedalaman pencerobohan, dan pengesanan pencerobohan perineural.',
            analyzeSlide: 'Analisis Slaid',
            clinicalScreening: 'Saringan Klinikal',
            clinicalScreeningDesc: 'Pengesanan objek masa nyata untuk mengenal pasti lesi, karies, dan kebimbangan kesihatan mulut yang kelihatan dari foto standard.',
            
            // CTA Section
            trustedHealthcare: 'PENJAGAAN KESIHATAN DIPERCAYAI',
            empoweringDetection: 'Memperkasakan Pengesanan Awal Menyelamatkan Nyawa.',
            empoweringDesc: 'Sertai ribuan pesakit dan doktor yang mempercayai Oral AI untuk saringan kesihatan mulut yang pantas, tepat, dan mudah diakses.',
            accuracyRate: 'Kadar Ketepatan',
            patientsScreened: 'Pesakit Disaring',
            aiAvailability: 'Ketersediaan AI',
            needExpertAdvice: 'Perlukan Nasihat Pakar?',
            expertAdviceDesc: 'Pasukan perubatan kami di sini untuk membantu mentafsir keputusan anda dan membimbing langkah seterusnya.',
            callUsNow: 'Hubungi Kami Sekarang',
            emailSupport: 'Sokongan E-mel',
            
            // Testimonials
            testimonials: 'TESTIMONI',
            whatPatientsSay: 'Apa Kata Pesakit Kami',
            realStories: 'Kisah sebenar daripada orang yang telah menggunakan alat saringan AI kami untuk pengesanan awal dan ketenangan fikiran.',
            patient: 'Pesakit',
            regularUser: 'Pengguna Tetap',
            dentalHygienist: 'Pakar Kebersihan Gigi',
            
            // Footer
            footerTagline: 'Mempelopori masa depan diagnostik pergigian dengan teknologi AI termaju. Penjagaan kesihatan yang tepat, pantas, dan mudah diakses untuk semua orang.',
            platform: 'Platform',
            aboutUs: 'Tentang Kami',
            ourTeams: 'Pasukan Kami',
            tryAITool: 'Cuba Alat AI',
            stayUpdated: 'Kekal Dikemaskini',
            newsletterDesc: 'Langgan surat berita kami untuk penemuan perubatan AI terkini.',
            enterYourEmail: 'Masukkan e-mel anda',
            join: 'Sertai',
            designedForHealthcare: 'Direka untuk penjagaan kesihatan yang lebih baik.',
            quickLinks: 'Pautan Pantas',
            resources: 'Sumber',
            legal: 'Undang-undang',
            privacyPolicy: 'Dasar Privasi',
            termsOfService: 'Terma Perkhidmatan',
            cookiePolicy: 'Dasar Kuki',
            hipaaCompliance: 'Pematuhan HIPAA',
            followUs: 'Ikuti Kami',
            allRightsReserved: 'Hak cipta terpelihara',
            
            // Additional Settings
            managePersonalInfo: 'Urus maklumat peribadi anda',
            patientRecords: 'Rekod Pesakit',
            managePatients: 'Urus pesakit berdaftar dan akaun mereka.',
            searchPatients: 'Cari pesakit mengikut nama atau e-mel...',
            loadingRecords: 'Memuatkan rekod...',
            id: 'ID',
            email: 'E-mel',
            status: 'Status',
            actions: 'Tindakan',
            
            // Home Page Hero - New Design
            trustedBy: 'Dipercayai oleh 10,000+ Profesional Kesihatan',
            heroLine1: 'Generasi Baharu',
            heroLine2: 'AI Kesihatan Mulut',
            heroLine3: 'Platform',
            schedule: 'Jadual',
            viewCalendar: 'Lihat Kalendar',
            accuracyRate: 'Kadar Ketepatan',
            analysisTime: 'Masa Analisis',
            compliant: 'Mematuhi',
            accuracy: 'Ketepatan',
            results: 'Keputusan',
            secure: 'Selamat',
            readyToScan: 'Sedia untuk Imbas',
            detection: 'Pengesanan',
            speed: 'Kelajuan',
            aiModels: 'Model AI',
            noIssues: 'Tiada Isu',
            detected: 'Dikesan',
            aiPowered: 'Dikuasakan AI',
            analysis: 'Analisis',
            scrollToExplore: 'Tatal untuk meneroka',
            
            // Quick Actions - New Design
            quickAccess: 'AKSES PANTAS',
            whatToDo: 'Apa yang anda ingin lakukan?',
            aiScreening: 'Saringan AI',
            analyzeImages: 'Analisis imej mulut dengan AI',
            scheduleVisit: 'Jadualkan lawatan seterusnya',
            manageSchedule: 'Urus jadual anda',
            getHelp: 'Dapatkan Bantuan',
            talkToExpert: 'Bercakap dengan pakar',
            aiAnalysis: 'Analisis AI',
            scheduleMeeting: 'Jadual Mesyuarat',
            viewReports: 'Lihat Laporan',
            analysisHistory: 'Sejarah Analisis',
            contactDoctor: 'Hubungi Doktor',
            getSupport: 'Dapatkan Sokongan',
            
            // Calendar Section
            appointmentCalendar: 'Kalendar Temujanji',
            calendarDesc: 'Lihat dan urus temujanji anda. Klik pada mana-mana tarikh untuk melihat butiran atau membuat temujanji baru.',
            loginToViewAppointments: 'Log masuk untuk melihat temujanji anda',
            upcomingAppointments: 'Temujanji Akan Datang',
            legend: 'Petunjuk',
            colorGuide: 'Panduan Warna',
            patientAppointments: 'Temujanji Pesakit',
            
            // Calendar & Booking
            dailySchedule: 'Jadual Harian',
            selectDate: 'Pilih tarikh',
            noAppointments: 'Tiada temujanji dijadualkan',
            enjoyFreeTime: 'Nikmati masa lapang anda, Doktor.',
            doctor: 'Doktor',
            time: 'Masa',
            dateTime: 'Tarikh & Masa',
            notes: 'Nota',
            noNotesProvided: 'Tiada nota disediakan',
            yourAppointments: 'Temujanji Anda',
            editAppointment: 'Edit Temujanji',
            saveChanges: 'Simpan Perubahan',
            
            // Guest Modal
            welcome: 'Selamat Datang!',
            needAccountToManage: 'Anda memerlukan akaun untuk mengurus temujanji.',
            logIn: 'Log Masuk',
            createAccount: 'Buat Akaun',
            
            // Login Page
            signIn: 'Log Masuk',
            signInTitle: 'Log Masuk',
            enterCredentials: 'Masukkan kelayakan anda untuk mengakses akaun anda',
            rememberMe: 'Ingat saya',
            forgotPassword: 'Lupa kata laluan?',
            signingIn: 'Sedang Log Masuk...',
            dontHaveAccount: 'Tiada akaun?',
            welcomeBack: 'Selamat Kembali.',
            loginDesc: 'Akses papan pemuka peribadi anda untuk mengurus temujanji, melihat laporan analisis, dan berhubung dengan profesional perubatan dengan lancar.',
            
            // Register Page
            joinUsToday: 'Sertai Kami Hari Ini.',
            registerDesc: 'Buat akaun untuk mengakses saringan AI mulut terkini, mengurus temujanji dengan pakar, dan jejaki perjalanan kesihatan mulut anda.',
            freeInitialScreening: 'Saringan AI Awal Percuma',
            secureMedicalRecords: 'Rekod Perubatan Selamat',
            directSpecialistBooking: 'Tempahan Pakar Langsung',
            fillDetails: 'Isi butiran anda untuk bermula',
            iAmA: 'Saya seorang...',
            patientRole: 'Pesakit (Saya mahu memeriksa kesihatan saya)',
            doctorRole: 'Profesional Perubatan (Saya mahu merawat)',
            creatingAccount: 'Mencipta Akaun...',
            alreadyHaveAccount: 'Sudah mempunyai akaun?',
            bySigningUp: 'Dengan mendaftar, anda bersetuju dengan',
            terms: 'Terma',
            and: '&',
            
            // About Page
            whoWeAre: 'Siapa Kami',
            aboutOralAI: 'Tentang Oral AI',
            aboutDesc: 'Mempelopori masa depan diagnostik pergigian melalui penggabungan kepakaran perubatan dan kecerdasan buatan termaju.',
            ourMission: 'Misi Kami',
            democratizingHealthcare: 'Mendemokrasikan Penjagaan Kesihatan Mulut Termaju',
            missionDesc: 'Misi kami adalah untuk menjadikan pengesanan penyakit mulut berkualiti tinggi dapat diakses oleh semua orang.',
            analysisAccuracy: 'Ketepatan Analisis',
            systemAvailability: 'Ketersediaan Sistem',
            ourCoreValues: 'Nilai Teras Kami',
            whatDrivesUs: 'Apa yang Mendorong Kami',
            patientFirst: 'Pesakit Didahulukan',
            patientFirstDesc: 'Setiap algoritma yang kami bangunkan dan setiap ciri yang kami bina direka dengan matlamat utama meningkatkan penjagaan dan keselamatan pesakit.',
            scientificRigor: 'Ketelitian Saintifik',
            scientificRigorDesc: 'Kami mematuhi standard tertinggi pengesahan saintifik. Model kami diuji dengan ketat dan sentiasa diperbaiki.',
            dataPrivacy: 'Privasi Data',
            dataPrivacyDesc: 'Kami melayan data pesakit dengan penuh hormat dan keselamatan, mematuhi semua peraturan perlindungan data penjagaan kesihatan utama.',
            ourTechnology: 'Teknologi Kami',
            poweredByInnovation: 'Dikuasakan oleh Inovasi',
            techDesc: 'Klik pada kad di bawah untuk meneroka alat canggih di sebalik AI kami.',
            deepLearningFramework: 'Rangka Kerja Pembelajaran Mendalam',
            explore: 'Teroka',
            
            // Contact Page
            getInTouch: 'Hubungi Kami',
            hereToHelp: 'Kami Di Sini Untuk Membantu',
            contactDesc: 'Ada soalan tentang teknologi AI kami atau perlukan sokongan? Hubungi pasukan kami.',
            contactInformation: 'Maklumat Hubungan',
            teamAvailable: 'Pasukan kami tersedia Isnin hingga Jumaat untuk membantu anda dengan sebarang pertanyaan.',
            emailUs: 'E-mel Kami',
            callUs: 'Hubungi Kami',
            visitUs: 'Lawati Kami',
            sendMessage: 'Hantar Mesej kepada Kami',
            subject: 'Subjek',
            message: 'Mesej',
            generalInquiry: 'Pertanyaan Umum',
            technicalSupport: 'Sokongan Teknikal',
            partnershipOpportunity: 'Peluang Perkongsian',
            pressMedia: 'Akhbar & Media',
            howCanWeHelp: 'Bagaimana kami boleh membantu anda?',
            supportCenter: 'Pusat Sokongan',
            faq: 'Soalan Lazim',
            faqDesc: 'Semua yang anda perlu tahu tentang teknologi dan perkhidmatan Oral AI.',
            
            // Triage/Analysis Page
            aiPoweredDiagnostics: 'DIAGNOSTIK BERKUASA AI',
            intelligentAnalysis: 'Analisis Penyakit Mulut Pintar',
            triageDesc: 'Menggunakan AI termaju untuk mengklasifikasikan imej klinikal dan slaid histopatologi dengan ketepatan.',
            dropImageHere: 'Lepaskan imej anda di sini, atau klik untuk melayari',
            supportsFormats: 'Menyokong JPG, JPEG, PNG (Klinikal atau Histopatologi)',
            secureUpload: 'Muat Naik Selamat & Peribadi',
            analyzingImage: 'Menganalisis Struktur Imej...',
            routingToModel: 'Menghalakan ke model pakar yang sesuai',
            systemCapabilities: 'Keupayaan Sistem',
            autoRouting: 'Penghalaan Auto',
            deepLearning: 'Pembelajaran Mendalam',
            objectDetection: 'Pengesanan Objek',
            triageSmartDesc: 'Secara automatik menghalakan imej yang dimuat naik ke model Histopatologi atau Saringan Klinikal berdasarkan ciri visual.',
            histopathologyDeepDesc: 'Analisis pembelajaran mendalam untuk pengesanan tumor, penggredan, dan pengukuran kedalaman pencerobohan pada slaid mikroskopik.',
            clinicalRealTimeDesc: 'Pengesanan objek masa nyata untuk penilaian kebersihan mulut dan pengenalpastian lesi atau keabnormalan yang berpotensi.',
            
            // Model A
            histopathologyAnalysis: 'Analisis Histopatologi',
            aiAnalysisInsight: 'Wawasan Analisis AI',
            loadingSuggestion: 'Memuatkan cadangan...',
            primaryDiagnosis: 'Diagnosis Utama',
            analyzing: 'Menganalisis...',
            confidence: 'Keyakinan',
            microscopicFeatures: 'Ciri Mikroskopik',
            depthOfInvasion: 'Kedalaman Pencerobohan',
            original: 'Asal',
            heatmap: 'Peta Haba',
            heatmapInfo: 'Peta haba memvisualisasikan kawasan tumor berkebarangkalian tinggi. Togol antara paparan untuk membandingkan.',
            
            // Model B
            clinicalAnalysis: 'Analisis Klinikal',
            detectedConditions: 'Keadaan yang Dikesan',
            noConditionsDetected: 'Tiada keadaan dikesan',
            
            // Chat Widget
            aiAssistant: 'Pembantu AI',
            onlineStatus: 'Dalam Talian - Sedia membantu',
            askAnything: 'Tanya apa-apa tentang kesihatan mulut...',
            typeMessage: 'Taip mesej anda...',
            send: 'Hantar',
            clearChat: 'Kosongkan Sembang',
            
            // Messages
            passwordUpdated: 'Kata laluan berjaya dikemas kini! Akaun anda kini lebih selamat.',
            passwordMismatch: 'Kata laluan baharu tidak sepadan! Sila cuba lagi.',
            passwordTooShort: 'Kata laluan baharu mestilah sekurang-kurangnya 6 aksara.',
            networkError: 'Ralat rangkaian. Sila semak sambungan anda dan cuba lagi.',
            languageChanged: 'Bahasa berjaya ditukar. Antara muka dikemas kini!',
            autoSaveEnabled: 'Auto-simpan diaktifkan. Laporan anda akan disimpan secara automatik.',
            autoSaveDisabled: 'Auto-simpan dinyahaktifkan. Anda perlu menyimpan laporan secara manual.',
            emailNotifEnabled: 'Pemberitahuan e-mel diaktifkan. Anda akan menerima kemas kini temujanji.',
            emailNotifDisabled: 'Pemberitahuan e-mel dinyahaktifkan. Anda tidak akan menerima e-mel temujanji.',
            profileUpdated: 'Profil berjaya dikemas kini!',
            pleaseEnterName: 'Sila masukkan nama yang sah',
            appointmentBooked: 'Temujanji Ditempah!',
            pleaseSelectTime: 'Sila pilih masa',
            failedToBook: 'Gagal menempah',
            sessionExpired: 'Sesi Tamat Tempoh',
            
            // Additional Login/Register
            loginBrandingDesc: 'Akses papan pemuka peribadi anda untuk mengurus temujanji, melihat laporan analisis, dan berhubung dengan profesional perubatan dengan lancar.',
            registerBrandingDesc: 'Cipta akaun untuk mengakses saringan mulut AI terkini, mengurus temujanji dengan pakar, dan menjejak perjalanan kesihatan mulut anda.',
            fillInDetails: 'Isikan butiran anda untuk bermula',
            rolePatient: 'Pesakit (Saya mahu memeriksa kesihatan saya)',
            roleDoctor: 'Profesional Perubatan (Saya mahu merawat)',
            fullNamePlaceholder: 'Ahmad bin Abdullah',
            emailPlaceholder: 'nama@contoh.com',
            copyrightText: '© 2026 Platform Oral AI. Hak cipta terpelihara.',
            appName: 'Oral AI',
            
            // About Page Additional
            aboutHeroDesc: 'Merintis masa depan diagnostik pergigian melalui gabungan kepakaran perubatan dan kecerdasan buatan termaju.',
            techSectionDesc: 'Klik pada kad di bawah untuk meneroka alat canggih di sebalik AI kami.',
            gpuAcceleration: 'Percepatan GPU',
            realTimeObjectDetection: 'Pengesanan Objek Masa Nyata',
            beginner: 'Pemula',
            advanced: 'Lanjutan',
            
            // Contact Page Additional
            contactHeroDesc: 'Ada soalan tentang teknologi AI kami atau perlukan sokongan? Hubungi pasukan kami.',
            teamAvailability: 'Pasukan kami tersedia Isnin hingga Jumaat untuk membantu anda dengan sebarang pertanyaan.',
            businessHours: 'Isn-Jum, 9pg - 6ptg',
            sendUsMessage: 'Hantarkan Mesej kepada Kami',
            messagePlaceholder: 'Bagaimana kami boleh membantu anda?',
            faqAccuracyQuestion: 'Sejauh mana ketepatan diagnosis AI?',
            faqAccuracyAnswer: 'Sistem dwi-model kami telah mencapai <strong>ketepatan 99.9%</strong> dalam ujian klinikal. Walau bagaimanapun, ia direka sebagai alat saringan dan tidak boleh menggantikan pemeriksaan doktor gigi profesional. Kami mengesyorkan menggunakannya untuk pengesanan awal dan pemantauan.',
            faqSecurityQuestion: 'Adakah data perubatan saya selamat?',
            faqSecurityAnswer: 'Ya. Kami mematuhi sepenuhnya <strong>HIPAA</strong> dan menggunakan penyulitan hujung ke hujung untuk semua imej dan data pesakit yang dimuat naik. Kami tidak menyimpan imej anda secara kekal tanpa persetujuan jelas anda, memastikan privasi anda sentiasa dilindungi.',
            faqApiQuestion: 'Bolehkah saya mengintegrasikan API ini ke dalam perisian klinik saya?',
            faqApiAnswer: 'Sudah tentu. Kami menawarkan API RESTful yang mantap yang direka untuk integrasi lancar dengan sistem Rekod Kesihatan Elektronik (EHR) sedia ada. Sila pilih "Peluang Perkongsian" dalam borang hubungan di atas untuk meminta dokumentasi dan kunci API.',
            faqTimeQuestion: 'Berapa lama analisis mengambil masa?',
            faqTimeAnswer: 'Analisis adalah hampir serta-merta. Enjin inferens optimum kami biasanya memproses imej resolusi tinggi dalam <strong>kurang daripada 2 saat</strong>, memberikan anda maklum balas segera dan laporan PDF yang boleh dimuat turun.',
            faqConditionsQuestion: 'Apakah keadaan yang boleh dikesan AI?',
            faqConditionsAnswer: 'Pada masa ini, model kami dilatih untuk mengesan tanda-tanda awal <strong>Gingivitis, Karies Gigi (Lubang), dan Periodontitis</strong>. Kami sedang aktif berusaha untuk mengembangkan set data kami untuk memasukkan saringan kanser mulut dan penilaian ortodontik.',
            
            // Triage Page Additional
            intelligentOralAnalysis: 'Analisis Penyakit Mulut Pintar',
            triageSubtitle: 'Menggunakan AI terkini untuk mengklasifikasikan imej klinikal dan slaid histopatologi dengan ketepatan. Muat naik sampel anda untuk memulakan proses triage automatik.',
            supportsImageFormats: 'Menyokong JPG, JPEG, PNG (Klinikal atau Histopatologi)',
            securePrivateUpload: 'Muat Naik Selamat & Peribadi',
            analyzingImageStructure: 'Menganalisis Struktur Imej...',
            smartTriageFeatureDesc: 'Secara automatik menghalakan imej yang dimuat naik ke model Histopatologi atau Saringan Klinikal berdasarkan ciri visual.',
            histopathologyFeatureDesc: 'Analisis pembelajaran mendalam untuk pengesanan tumor, penggredan, dan pengukuran kedalaman pencerobohan pada slaid mikroskopik.',
            clinicalScreeningFeatureDesc: 'Pengesanan objek masa nyata untuk penilaian kebersihan mulut dan pengenalan lesi atau keabnormalan yang berpotensi.',
            
            // Model A Additional
            toggleFullscreen: 'Togol Skrin Penuh',
            heatmapInfoNote: 'Peta haba memvisualisasikan kawasan tumor kebarangkalian tinggi. Togol antara paparan untuk membandingkan.',
            patternOfInvasion: 'Corak Pencerobohan',
            perineuralInvasion: 'Pencerobohan Perineural',
            mitoticIndex: 'Indeks Mitotik',
            tumourBudsCount: 'Kiraan Tunas Tumor',
            viewAiRecommendation: 'Lihat Cadangan AI',
            pdfReport: 'Laporan PDF',
            emailReport: 'E-mel Laporan',
            startNewAnalysis: 'Mulakan Analisis Baharu',
            
            // Model B Additional
            lowQualityImage: 'Imej Kualiti Rendah',
            detections: 'Pengesanan',
            fullscreen: 'Skrin Penuh',
            screeningResult: 'Keputusan Saringan',
            hygieneScore: 'Skor Kebersihan',
            waitingForAnalysis: 'Menunggu analisis...',
            
            // Chat Widget Additional
            oralAiAssistant: 'Pembantu Oral AI',
            onlineReady: 'Dalam Talian & Sedia',
            minimize: 'Kecilkan',
            chatWelcomeMessage: 'Hai! Saya pembantu perubatan AI anda. Saya boleh membantu menerangkan keputusan analisis anda atau menjawab soalan umum tentang kesihatan mulut.',
            justNow: 'BARU SAHAJA',
            suggestedTopics: 'Topik Dicadangkan',
            whatIsOralCancer: 'Apa itu Kanser Mulut?',
            explainHistopathology: 'Terangkan Histopatologi',
            howDoesAiWork: 'Bagaimana AI berfungsi?',
            chatInputPlaceholder: 'Taipkan soalan anda...',
            aiDisclaimer: 'AI boleh membuat kesilapan. Sahkan maklumat penting.',
            
            // Department Page
            ourExperts: 'Pakar Kami',
            meetTheTeam: 'Temui Pasukan',
            departmentHeroDesc: 'Minda cemerlang di sebalik Oral AI, berdedikasi untuk merevolusikan diagnostik pergigian melalui kerjasama dan inovasi.',
            systems: 'SISTEM',
            backendDesign: 'Reka Bentuk Backend',
            backendDeveloper: 'Pembangun Backend',
            backendDevDesc: 'Membina API yang mantap dan mengurus enjin inferens model berprestasi tinggi.',
            uiux: 'UI/UX',
            frontendDesign: 'Reka Bentuk Frontend',
            frontendDeveloper: 'Pembangun Frontend',
            frontendDevDesc: 'Mencipta antara muka pengguna intuitif dan responsif untuk analisis perubatan yang lancar.',
            dataTeam: 'PASUKAN DATA',
            datasetAnnotation: 'Anotasi & Penyediaan Set Data',
            datasetAnnotationDesc: 'Memastikan data berkualiti tinggi untuk melatih model AI kami.',
            datasetSpecialist: 'Pakar Set Data',
            datasetSpecialistDesc1: 'Pakar dalam anotasi imej perubatan dan saluran prapemprosesan data.',
            datasetSpecialistDesc2: 'Mengkhusus dalam jaminan kualiti data dan teknik pengimbangan set data.',
            datasetSpecialistDesc3: 'Fokus pada pengekstrakan ciri patologi dan pengurusan metadata.',
            
            // Blog Page
            oralAiJournal: 'Jurnal Oral AI',
            blogHeroTitle: 'Pandangan, Kemas Kini & Cerita',
            blogHeroDesc: 'Penyelaman mendalam ke dalam teknologi kami, panduan kesihatan pesakit, dan masa depan AI dalam pergigian.',
            engineering: 'Kejuruteraan',
            featuredPostTitle: 'Seni Bina Ketepatan: Di Dalam Sistem Dwi-Model Oral AI',
            featuredPostDesc: 'Bagaimana kami menggabungkan Penghala Triage dengan model Klinikal dan Histopatologi khusus untuk mencapai ketepatan diagnostik 99.8%.',
            readArticle: 'Baca Artikel',
            ourBlog: 'Blog Kami',
            latestArticles: 'Artikel Terkini',
            patientHealth: 'Kesihatan Pesakit',
            blogPost1Title: '5 Tanda Awal Masalah Kesihatan Mulut Yang Tidak Boleh Diabaikan',
            blogPost1Desc: 'Dari perubahan warna halus hingga sensitiviti ringan, pelajari apa yang mulut anda cuba beritahu sebelum ia menjadi masalah besar.',
            behindTheScenes: 'Di Sebalik Tabir',
            blogPost2Title: 'Dari Data ke Diagnosis: Bagaimana Kami Membina Set Data Kami',
            blogPost2Desc: 'Pandangan ke proses kurasi ketat yang digunakan Pasukan Set Data kami untuk memastikan AI kami belajar dari imej perubatan berkualiti tinggi.',
            futureTech: 'Teknologi Masa Depan',
            blogPost3Title: 'Masa Depan Tele-Pergigian: AI sebagai Responden Pertama',
            blogPost3Desc: 'Bayangkan mendapatkan diagnosis awal dari telefon pintar anda. Begini cara Oral AI menjadikan saringan jarak jauh satu realiti.',
            
            // News/Pages Page
            industryInsights: 'Pandangan Industri',
            eraOfMedicalAi: 'Era AI Perubatan',
            pagesHeroDesc: 'Temui bagaimana Kecerdasan Buatan sedang mengubah landskap penjagaan kesihatan, dari diagnosis awal hingga pelan rawatan peribadi.',
            diagnostics: 'Diagnostik',
            newsArticle1Title: 'AI Mengatasi Pakar Manusia dalam Pengesanan Awal Kanser',
            newsArticle1Desc: 'Kajian terkini menunjukkan model pembelajaran mendalam mencapai ketepatan 99% dalam mengenal pasti anomali peringkat awal dalam pengimejan perubatan, mengurangkan negatif palsu dengan ketara.',
            readFullStory: 'Baca Cerita Penuh',
            robotics: 'Robotik',
            newsArticle2Title: 'Pembedahan Ketepatan: Kebangkitan Operasi Berbantukan AI',
            newsArticle2Desc: 'Pakar bedah kini menggunakan lengan robotik berkuasa AI untuk melakukan prosedur kompleks dengan ketepatan sub-milimeter, meminimumkan masa pemulihan pesakit.',
            pharma: 'Farmaseutikal',
            newsArticle3Title: 'Mempercepatkan Penemuan Ubat',
            newsArticle3Desc: 'AI Generatif sedang memendekkan garis masa pembangunan ubat dari tahun ke bulan dengan meramalkan interaksi molekul.',
            genomics: 'Genomik',
            newsArticle4Title: 'Perubatan Hiper-Peribadi',
            newsArticle4Desc: 'Algoritma AI yang menganalisis data genomik kini boleh menyesuaikan pelan rawatan khusus untuk profil DNA individu.',
            patientCare: 'Penjagaan Pesakit',
            newsArticle5Title: 'Pembantu Kesihatan Maya 24/7',
            newsArticle5Desc: 'Chatbot berkuasa LLM menyediakan triage perubatan segera dan tepat serta sokongan kesihatan mental di seluruh dunia.',
            joinTheRevolution: 'Sertai Revolusi',
            joinRevolutionDesc: 'Oral AI berada di barisan hadapan transformasi ini. Alami alat diagnostik canggih kami hari ini.',
            tryOralAiNow: 'Cuba Oral AI Sekarang',
            
            // CTA Section
            trustedHealthcare: 'PENJAGAAN KESIHATAN DIPERCAYAI',
            empoweringEarlyDetection: 'Memperkasa Pengesanan Awal<br>Menyelamatkan Nyawa.',
            joinThousandsDesc: 'Sertai ribuan pesakit dan klinisi yang mempercayai Oral AI untuk saringan kesihatan mulut yang pantas, tepat dan mudah diakses.',
            accuracyRate: 'Kadar Ketepatan',
            patientsScreened: 'Pesakit Disaring',
            aiAvailability: 'Ketersediaan AI',
            supportLabel: 'SOKONGAN',
            needExpertAdvice: 'Perlu Nasihat Pakar?',
            medicalTeamHelp: 'Pasukan perubatan kami sedia membantu mentafsir keputusan anda dan membimbing langkah seterusnya.',
            callUsNow: 'Hubungi Kami Sekarang',
            emailSupport: 'Sokongan E-mel',
            
            // Testimonials
            testimonialsLabel: 'TESTIMONI',
            whatPatientsSay: 'Apa Kata Pesakit Kami',
            testimonialsDesc: 'Kisah sebenar daripada orang yang telah menggunakan alat saringan AI kami untuk pengesanan awal dan ketenangan fikiran.',
            testimonial1: '"Saringan AI sangat pantas. Saya bimbang tentang tompok pada gusi saya, dan alat ini memberi penilaian segera yang membantu saya membuat keputusan untuk berjumpa doktor."',
            testimonial2: '"Sebagai perokok, saya bimbang tentang kesihatan mulut. Aplikasi ini membantu saya menjejaki perubahan. Penjanaan laporan sangat profesional dan mudah difahami."',
            testimonial3: '"Saya mengesyorkan ini kepada pesakit saya untuk pemantauan sendiri antara lawatan. Ketepatan pengesanan lesi sangat mengagumkan dan boleh dipercayai."',
            testimonial4: '"Antara muka sangat mudah digunakan. Saya hanya memuat naik foto dan mendapat keputusan dalam beberapa saat. Ia memberi ketenangan fikiran apabila saya memerlukannya."',
            testimonial5: '"Alat yang hebat untuk tujuan pendidikan juga. Ia membantu memvisualisasikan rupa keadaan mulut yang berbeza. Sangat membantu untuk pelajar."',
            testimonial6: '"Saya mempunyai kebimbangan tentang luka yang tidak sembuh. Aplikasi mencadangkan saya berjumpa pakar, dan saya gembira saya berbuat demikian. Pengesanan awal berkesan."',
            rolePatient: 'Pesakit',
            roleRegularUser: 'Pengguna Biasa',
            roleDentalHygienist: 'Ahli Kebersihan Pergigian',
            roleStudent: 'Pelajar',
            roleDoctor: 'Doktor',
            roleAdmin: 'Pentadbir',
            
            // Notifications
            notificationsTitle: 'Pemberitahuan',
            markAllRead: 'Tandakan semua dibaca',
            noNewNotifications: 'Tiada pemberitahuan baharu',
            allCaughtUp: 'Semua Selesai!',
            noNewNotificationsOrAppointments: 'Tiada pemberitahuan atau temu janji baharu.',
            
            // Model B Results
            qualityNoteLowRes: 'Resolusi Rendah. Beralih ke Mod Standard untuk kestabilan lebih baik.',
            screeningResultNormal: 'Normal',
            screeningResultRefertoDentist: 'Rujuk kepada Doktor Gigi',
            hygieneScoreHigh: 'Tinggi',
            hygieneScoreMedium: 'Sederhana',
            hygieneScoreLow: 'Rendah',
            noIssuesDetected: 'Tiada isu khusus dikesan.',
            detectedCount: '{count} dikesan',
            conditionCaries: 'Karies',
            conditionGingivitis: 'Gingivitis',
            conditionUlcer: 'Ulser',
            conditionTooth: 'Gigi',
            conditionCalculus: 'Kalkulus',
            conditionHypodontia: 'Hipodontia',
            
            // Model A Results
            tumourDetected: 'Tumor Dikesan',
            noTumour: 'Tiada Tumor',
            detected: 'Dikesan',
            notDetected: 'Tidak Dikesan',
            
            // Technology Modal
            techPytorchSubtitle: 'Rangka Kerja Pembelajaran Mendalam',
            techPytorchBeginner: "PyTorch, dibangunkan oleh Facebook, adalah rangka kerja pembelajaran mendalam yang digunakan secara meluas untuk membina rangkaian neural. Sifat Pythonic yang mudah menjadikannya senang untuk pemula memahami asas penciptaan dan latihan model. Pemula akan menghargai fleksibiliti PyTorch dalam mencipta model mudah untuk klasifikasi imej tanpa perlu risau tentang overhead teknikal yang berlebihan.",
            techPytorchAdvanced: "Pengguna lanjutan boleh menggunakan graf pengiraan dinamik PyTorch, membolehkan fleksibiliti lebih besar semasa membina seni bina kompleks, fungsi kerugian tersuai dan pengoptimum. Ia pilihan hebat untuk penyelidik, kerana PyTorch menawarkan eksperimen lancar dengan model canggih seperti Model Bahasa Penglihatan, Rangkaian Adversarial Generatif (GAN) dan pembelajaran pengukuhan mendalam. Terima kasih kepada pengurusan memori yang cekap dan sokongan GPU, ia juga cemerlang dalam mengendalikan set data besar.",
            techCudaSubtitle: 'Pecutan GPU',
            techCudaBeginner: "CUDA adalah platform pengkomputeran selari dan model pengaturcaraan yang dibangunkan oleh NVIDIA, manakala cuDNN adalah perpustakaan dipercepatkan GPU untuk rangkaian neural dalam. Untuk pemula, alat-alat ini mungkin kelihatan teknikal, tetapi tujuan utama mereka adalah untuk mempercepatkan latihan model pembelajaran mendalam dengan menggunakan kuasa GPU. Dengan menyediakan CUDA dan cuDNN dengan betul dalam persekitaran latihan, peningkatan kelajuan dan pengoptimuman latihan model yang ketara boleh dicapai, terutamanya apabila bekerja dengan rangka kerja seperti TensorFlow dan PyTorch.",
            techCudaAdvanced: "Pakar boleh memanfaatkan kuasa penuh CUDA dan cuDNN untuk mengoptimumkan prestasi dalam aplikasi permintaan tinggi. Ini termasuk menulis kernel CUDA tersuai untuk operasi khusus, mengurus memori GPU dengan cekap, dan menala halus latihan rangkaian neural untuk kelajuan dan skalabiliti maksimum. Alat-alat ini penting untuk pembangun yang bekerja dengan set data besar dan memerlukan prestasi terbaik daripada model mereka.",
            techYoloSubtitle: 'Pengesanan Objek Masa Nyata',
            techYoloBeginner: "YOLO (You Only Look Once) adalah algoritma pengesanan objek pantas yang sangat popular untuk aplikasi masa nyata. Pemula boleh menggunakan model YOLO pra-latihan untuk mengesan objek dalam imej atau video dengan cepat menggunakan kod yang agak mudah. Kemudahan penggunaan menjadikan YOLO titik masuk yang hebat bagi mereka yang ingin meneroka pengesanan objek tanpa perlu membina model kompleks dari awal.",
            techYoloAdvanced: "YOLO menyediakan peluang untuk menala halus model pada set data tersuai untuk mengesan objek khusus, meningkatkan kelajuan dan ketepatan pengesanan. Sifat ringan YOLO membolehkannya digunakan dalam persekitaran terhad sumber, seperti peranti mudah alih, menjadikannya penyelesaian pilihan untuk aplikasi masa nyata. Profesional juga boleh bereksperimen dengan versi YOLO yang lebih baharu, menyesuaikan parameter untuk memenuhi keperluan projek khusus."
        },
        zh: {
            // Navigation
            home: '首页',
            about: '关于',
            services: '服务',
            department: '部门',
            news: '新闻',
            blog: '博客',
            contact: '联系',
            login: '登录',
            signUp: '注册',
            logout: '登出',
            myProfile: '我的资料',
            settings: '设置',
            
            // Common Buttons & Actions
            save: '保存',
            saveChanges: '保存更改',
            cancel: '取消',
            close: '关闭',
            submit: '提交',
            delete: '删除',
            edit: '编辑',
            search: '搜索',
            loading: '加载中...',
            updating: '更新中...',
            change: '更改',
            viewMore: '查看更多',
            learnMore: '了解更多',
            getStarted: '开始',
            bookAppointment: '预约',
            discoverMore: '了解更多',
            startScreening: '开始筛查',
            tryNow: '立即尝试',
            
            // Status & Feedback
            error: '错误',
            success: '成功',
            warning: '警告',
            info: '信息',
            
            // Profile & Settings
            fullName: '全名',
            emailAddress: '电子邮件地址',
            password: '密码',
            currentPassword: '当前密码',
            newPassword: '新密码',
            confirmPassword: '确认新密码',
            changePassword: '更改密码',
            updatePassword: '更新密码',
            enterCurrentPassword: '输入当前密码',
            enterNewPassword: '输入新密码',
            confirmNewPassword: '确认新密码',
            emailCannotChange: '出于安全考虑，无法更改电子邮件。',
            changeYourPassword: '更改您的帐户密码',
            lastChanged: '上次更改',
            
            // Settings Page
            general: '常规',
            security: '安全',
            patientManagement: '患者管理',
            generalPreferences: '常规设置',
            securitySettings: '安全设置',
            languageRegion: '语言和地区',
            preferredLanguage: '首选语言',
            selectLanguage: '选择您的界面首选语言',
            reportSettings: '报告设置',
            autoSaveReports: '自动保存报告',
            autoSaveDesc: '自动将分析报告保存到您的帐户',
            notifications: '通知',
            emailNotifications: '电子邮件通知',
            emailNotifDesc: '接收有关预约的更新',
            passwordChangeInfo: '密码更改需要重新验证。',
            
            // Home Page Hero
            welcomeTitle: 'AI驱动的预约和疾病检测',
            welcomeSubtitle: '无缝管理患者预约，使用最先进的AI进行专业级分析，及早发现口腔癌。',
            advancedOralHealth: '高级口腔健康',
            viewCalendar: '查看日历',
            accuracyRate: '准确率',
            analysisTime: '分析时间',
            compliant: '合规',
            
            // New Hero Section
            trustedBy: '受到10,000+医疗专业人员的信赖',
            heroLine1: '新一代',
            heroLine2: '口腔健康AI',
            heroLine3: '平台',
            accuracy: '准确率',
            results: '结果',
            secure: '安全',
            readyToScan: '准备扫描',
            detection: '检测',
            speed: '速度',
            aiModels: 'AI模型',
            noIssues: '未检测到',
            detected: '问题',
            aiPowered: 'AI驱动',
            analysis: '分析',
            scrollToExplore: '滚动探索',
            
            // Quick Actions (New)
            quickAccess: '快速访问',
            whatToDo: '今天您想做什么？',
            aiScreening: 'AI筛查',
            analyzeImages: '分析图像',
            scheduleVisit: '预约就诊',
            manageSchedule: '管理日程',
            getHelp: '获取帮助',
            talkToExpert: '咨询专家',
            
            // Quick Actions
            aiAnalysis: 'AI分析',
            scheduleMeeting: '安排会议',
            viewReports: '查看报告',
            analysisHistory: '分析历史',
            contactDoctor: '联系医生',
            getSupport: '获取支持',
            
            // Calendar Section
            appointmentCalendar: '预约日历',
            calendarDesc: '查看和管理您的预约。点击任何日期查看详情或预约新的预约。',
            loginToViewAppointments: '登录查看您的预约',
            upcomingAppointments: '即将到来的预约',
            legend: '图例',
            colorGuide: '颜色指南',
            patientAppointments: '患者预约',
            
            // Why Choose Section
            whyChooseTitle: '为什么选择Oral AI？',
            whyChooseHeading: '将医学专业知识与人工智能相结合',
            whyChooseDesc: '我们为牙科专业人员提供第二意见AI工具，比以往更快、更准确地检测异常。',
            instantResults: '即时结果',
            instantResultsDesc: '实时分析',
            highPrecision: '高精度',
            highPrecisionDesc: '微观细节',
            secureData: '安全数据',
            secureDataDesc: 'HIPAA合规',
            expertSupport: '专家支持',
            expertSupportDesc: '由医生验证',
            
            // Services Section
            ourServices: '我们的服务',
            comprehensiveAnalysis: '全面AI分析',
            comprehensiveAnalysisDesc: '我们的多模型架构确保每个案例都由专为该特定模式设计的专业算法处理。',
            smartTriage: '智能分诊',
            smartTriageDesc: '智能路由系统，自动分类上传的图像并将其引导到适当的诊断模型。',
            tryTriage: '尝试分诊',
            histopathology: '组织病理学',
            histopathologyDesc: '显微分析，用于精确的肿瘤分级、侵袭深度测量和神经周围侵袭检测。',
            analyzeSlide: '分析切片',
            clinicalScreening: '临床筛查',
            clinicalScreeningDesc: '实时物体检测，从标准照片中识别病变、龋齿和其他可见的口腔健康问题。',
            
            // CTA Section
            trustedHealthcare: '值得信赖的医疗保健',
            empoweringDetection: '赋能早期检测 拯救生命',
            empoweringDesc: '加入数千名信任Oral AI进行快速、准确和可访问的口腔健康筛查的患者和临床医生。',
            accuracyRate: '准确率',
            patientsScreened: '筛查患者',
            aiAvailability: 'AI可用性',
            needExpertAdvice: '需要专家建议？',
            expertAdviceDesc: '我们的医疗团队在这里帮助解释您的结果并指导您的下一步行动。',
            callUsNow: '立即致电',
            emailSupport: '电子邮件支持',
            
            // Testimonials
            testimonials: '客户评价',
            whatPatientsSay: '患者的评价',
            realStories: '来自使用我们的AI筛查工具进行早期检测和安心的人们的真实故事。',
            patient: '患者',
            regularUser: '常规用户',
            dentalHygienist: '牙科保健师',
            
            // Footer
            footerTagline: '以先进的AI技术开拓牙科诊断的未来。准确、快速、易于获得的医疗保健，为每个人服务。',
            platform: '平台',
            aboutUs: '关于我们',
            ourTeams: '我们的团队',
            tryAITool: '试用AI工具',
            stayUpdated: '保持更新',
            newsletterDesc: '订阅我们的新闻通讯，获取最新的AI医学突破。',
            enterYourEmail: '输入您的电子邮件',
            join: '加入',
            designedForHealthcare: '为更好的医疗保健而设计。',
            quickLinks: '快速链接',
            resources: '资源',
            legal: '法律',
            privacyPolicy: '隐私政策',
            termsOfService: '服务条款',
            cookiePolicy: 'Cookie政策',
            hipaaCompliance: 'HIPAA合规',
            followUs: '关注我们',
            allRightsReserved: '版权所有',
            
            // Additional Settings
            managePersonalInfo: '管理您的个人信息',
            patientRecords: '患者记录',
            managePatients: '管理已注册的患者及其账户。',
            searchPatients: '按姓名或电子邮件搜索患者...',
            loadingRecords: '正在加载记录...',
            id: 'ID',
            email: '电子邮件',
            status: '状态',
            actions: '操作',
            schedule: '日程',
            
            // Calendar & Booking
            dailySchedule: '每日日程',
            selectDate: '选择日期',
            noAppointments: '没有预约',
            enjoyFreeTime: '享受您的空闲时间，医生。',
            doctor: '医生',
            time: '时间',
            dateTime: '日期和时间',
            notes: '备注',
            noNotesProvided: '未提供备注',
            yourAppointments: '您的预约',
            editAppointment: '编辑预约',
            saveChanges: '保存更改',
            
            // Guest Modal
            welcome: '欢迎！',
            needAccountToManage: '您需要一个账户来管理预约。',
            logIn: '登录',
            createAccount: '创建账户',
            
            // Login Page
            signIn: '登录',
            signInTitle: '登录',
            enterCredentials: '输入您的凭据以访问您的账户',
            rememberMe: '记住我',
            forgotPassword: '忘记密码？',
            signingIn: '正在登录...',
            dontHaveAccount: '没有账户？',
            welcomeBack: '欢迎回来。',
            loginDesc: '访问您的个人仪表板，管理预约、查看分析报告，并与医疗专业人员无缝连接。',
            
            // Register Page
            joinUsToday: '今天加入我们。',
            registerDesc: '创建账户以访问最先进的AI口腔筛查，与专家预约，并跟踪您的口腔健康旅程。',
            freeInitialScreening: '免费初始AI筛查',
            secureMedicalRecords: '安全的医疗记录',
            directSpecialistBooking: '直接专家预约',
            fillDetails: '填写您的详细信息以开始',
            iAmA: '我是...',
            patientRole: '患者（我想检查我的健康）',
            doctorRole: '医疗专业人员（我想治疗）',
            creatingAccount: '正在创建账户...',
            alreadyHaveAccount: '已经有账户？',
            bySigningUp: '注册即表示您同意我们的',
            terms: '条款',
            and: '和',
            
            // About Page
            whoWeAre: '我们是谁',
            aboutOralAI: '关于Oral AI',
            aboutDesc: '通过医学专业知识和先进人工智能的融合，开创牙科诊断的未来。',
            ourMission: '我们的使命',
            democratizingHealthcare: '普及先进口腔健康护理',
            missionDesc: '我们的使命是让每个人都能获得高质量的口腔疾病检测。',
            analysisAccuracy: '分析准确率',
            systemAvailability: '系统可用性',
            ourCoreValues: '我们的核心价值观',
            whatDrivesUs: '驱动我们的是什么',
            patientFirst: '患者优先',
            patientFirstDesc: '我们开发的每个算法和构建的每个功能都旨在改善患者护理和安全。',
            scientificRigor: '科学严谨',
            scientificRigorDesc: '我们坚持最高标准的科学验证。我们的模型经过严格测试并不断改进。',
            dataPrivacy: '数据隐私',
            dataPrivacyDesc: '我们以最高的尊重和安全性对待患者数据，遵守所有主要的医疗数据保护法规。',
            ourTechnology: '我们的技术',
            poweredByInnovation: '由创新驱动',
            techDesc: '点击下面的卡片，探索我们AI背后的尖端工具。',
            deepLearningFramework: '深度学习框架',
            explore: '探索',
            
            // Contact Page
            getInTouch: '联系我们',
            hereToHelp: '我们在这里帮助您',
            contactDesc: '对我们的AI技术有疑问或需要支持？联系我们的团队。',
            contactInformation: '联系信息',
            teamAvailable: '我们的团队周一至周五可为您提供任何咨询。',
            emailUs: '发送邮件',
            callUs: '致电我们',
            visitUs: '访问我们',
            sendMessage: '发送消息',
            subject: '主题',
            message: '消息',
            generalInquiry: '一般咨询',
            technicalSupport: '技术支持',
            partnershipOpportunity: '合作机会',
            pressMedia: '媒体',
            howCanWeHelp: '我们如何帮助您？',
            supportCenter: '支持中心',
            faq: '常见问题',
            faqDesc: '关于Oral AI技术和服务的所有信息。',
            
            // Triage/Analysis Page
            aiPoweredDiagnostics: 'AI驱动的诊断',
            intelligentAnalysis: '智能口腔疾病分析',
            triageDesc: '部署最先进的AI，精确分类临床图像和组织病理学切片。',
            dropImageHere: '将图像拖放到此处，或点击浏览',
            supportsFormats: '支持JPG、JPEG、PNG（临床或组织病理学）',
            secureUpload: '安全和私密上传',
            analyzingImage: '正在分析图像结构...',
            routingToModel: '正在路由到适当的专业模型',
            systemCapabilities: '系统能力',
            autoRouting: '自动路由',
            deepLearning: '深度学习',
            objectDetection: '物体检测',
            triageSmartDesc: '根据视觉特征自动将上传的图像路由到组织病理学或临床筛查模型。',
            histopathologyDeepDesc: '深度学习分析，用于显微切片上的肿瘤检测、分级和侵袭深度测量。',
            clinicalRealTimeDesc: '实时物体检测，用于口腔卫生评估和潜在病变或异常的识别。',
            
            // Model A
            histopathologyAnalysis: '组织病理学分析',
            aiAnalysisInsight: 'AI分析洞察',
            loadingSuggestion: '正在加载建议...',
            primaryDiagnosis: '主要诊断',
            analyzing: '分析中...',
            confidence: '置信度',
            microscopicFeatures: '显微特征',
            depthOfInvasion: '侵袭深度',
            original: '原始',
            heatmap: '热图',
            heatmapInfo: '热图可视化高概率肿瘤区域。在视图之间切换以进行比较。',
            
            // Model B
            clinicalAnalysis: '临床分析',
            detectedConditions: '检测到的状况',
            noConditionsDetected: '未检测到状况',
            
            // Chat Widget
            aiAssistant: 'AI助手',
            onlineStatus: '在线 - 随时帮助',
            askAnything: '询问有关口腔健康的任何问题...',
            typeMessage: '输入您的消息...',
            send: '发送',
            clearChat: '清除聊天',
            
            // Messages
            passwordUpdated: '密码更新成功！您的帐户现在更安全。',
            passwordMismatch: '新密码不匹配！请重试。',
            passwordTooShort: '新密码必须至少6个字符。',
            networkError: '网络错误。请检查您的连接并重试。',
            languageChanged: '语言更改成功。界面已更新！',
            autoSaveEnabled: '自动保存已启用。您的报告将自动保存。',
            autoSaveDisabled: '自动保存已禁用。您需要手动保存报告。',
            emailNotifEnabled: '电子邮件通知已启用。您将收到预约更新。',
            emailNotifDisabled: '电子邮件通知已禁用。您将不会收到预约电子邮件。',
            profileUpdated: '资料更新成功！',
            pleaseEnterName: '请输入有效的姓名',
            appointmentBooked: '预约已确认！',
            pleaseSelectTime: '请选择时间',
            failedToBook: '预约失败',
            sessionExpired: '会话已过期',
            
            // Additional Login/Register
            loginBrandingDesc: '访问您的个性化仪表板，管理预约、查看分析报告，并与医疗专业人员无缝连接。',
            registerBrandingDesc: '创建账户以访问最先进的AI口腔筛查、与专家预约，并跟踪您的口腔健康历程。',
            fillInDetails: '填写您的详细信息以开始',
            rolePatient: '患者（我想检查我的健康）',
            roleDoctor: '医疗专业人员（我想治疗）',
            fullNamePlaceholder: '张三',
            emailPlaceholder: 'name@example.com',
            copyrightText: '© 2026 Oral AI 平台。保留所有权利。',
            appName: 'Oral AI',
            
            // About Page Additional
            aboutHeroDesc: '通过医学专业知识与先进人工智能的融合，开创牙科诊断的未来。',
            techSectionDesc: '点击下面的卡片，探索我们AI背后的尖端工具。',
            gpuAcceleration: 'GPU加速',
            realTimeObjectDetection: '实时目标检测',
            beginner: '初学者',
            advanced: '高级',
            
            // Contact Page Additional
            contactHeroDesc: '对我们的AI技术有疑问或需要支持？联系我们的团队。',
            teamAvailability: '我们的团队周一至周五可为您提供任何咨询。',
            businessHours: '周一至周五，上午9点-下午6点',
            sendUsMessage: '给我们发送消息',
            messagePlaceholder: '我们如何帮助您？',
            faqAccuracyQuestion: 'AI诊断的准确度如何？',
            faqAccuracyAnswer: '我们的双模型系统在临床试验中达到了<strong>99.9%的准确率</strong>。然而，它被设计为筛查工具，不应取代专业牙医的检查。我们建议将其用于早期检测和监测。',
            faqSecurityQuestion: '我的医疗数据安全吗？',
            faqSecurityAnswer: '是的。我们完全符合<strong>HIPAA</strong>标准，并对所有上传的图像和患者数据使用端到端加密。未经您的明确同意，我们不会永久存储您的图像，确保您的隐私始终得到保护。',
            faqApiQuestion: '我可以将此API集成到我诊所的软件中吗？',
            faqApiAnswer: '当然可以。我们提供强大的RESTful API，旨在与现有的电子健康记录（EHR）系统无缝集成。请在上面的联系表单中选择"合作机会"来请求文档和API密钥。',
            faqTimeQuestion: '分析需要多长时间？',
            faqTimeAnswer: '分析几乎是即时的。我们优化的推理引擎通常在<strong>不到2秒</strong>内处理高分辨率图像，为您提供即时反馈和可下载的PDF报告。',
            faqConditionsQuestion: 'AI可以检测哪些状况？',
            faqConditionsAnswer: '目前，我们的模型被训练用于检测<strong>牙龈炎、龋齿（蛀牙）和牙周炎</strong>的早期迹象。我们正在积极扩展我们的数据集，以包括口腔癌筛查和正畸评估。',
            
            // Triage Page Additional
            intelligentOralAnalysis: '智能口腔疾病分析',
            triageSubtitle: '部署最先进的AI，精确分类临床图像和组织病理学切片。上传您的样本以开始自动分诊过程。',
            supportsImageFormats: '支持JPG、JPEG、PNG（临床或组织病理学）',
            securePrivateUpload: '安全和私密上传',
            analyzingImageStructure: '正在分析图像结构...',
            smartTriageFeatureDesc: '根据视觉特征自动将上传的图像路由到组织病理学或临床筛查模型。',
            histopathologyFeatureDesc: '深度学习分析，用于显微切片上的肿瘤检测、分级和侵袭深度测量。',
            clinicalScreeningFeatureDesc: '实时物体检测，用于口腔卫生评估和潜在病变或异常的识别。',
            
            // Model A Additional
            toggleFullscreen: '切换全屏',
            heatmapInfoNote: '热图可视化高概率肿瘤区域。在视图之间切换以进行比较。',
            patternOfInvasion: '侵袭模式',
            perineuralInvasion: '神经周围侵袭',
            mitoticIndex: '有丝分裂指数',
            tumourBudsCount: '肿瘤芽计数',
            viewAiRecommendation: '查看AI建议',
            pdfReport: 'PDF报告',
            emailReport: '电子邮件报告',
            startNewAnalysis: '开始新分析',
            
            // Model B Additional
            lowQualityImage: '低质量图像',
            detections: '检测',
            fullscreen: '全屏',
            screeningResult: '筛查结果',
            hygieneScore: '卫生评分',
            waitingForAnalysis: '等待分析...',
            
            // Chat Widget Additional
            oralAiAssistant: 'Oral AI助手',
            onlineReady: '在线并就绪',
            minimize: '最小化',
            chatWelcomeMessage: '您好！我是您的AI医疗助手。我可以帮助解释您的分析结果或回答有关口腔健康的一般问题。',
            justNow: '刚刚',
            suggestedTopics: '建议主题',
            whatIsOralCancer: '什么是口腔癌？',
            explainHistopathology: '解释组织病理学',
            howDoesAiWork: 'AI是如何工作的？',
            chatInputPlaceholder: '输入您的问题...',
            aiDisclaimer: 'AI可能会出错。请验证重要信息。',
            
            // Department Page
            ourExperts: '我们的专家',
            meetTheTeam: '认识团队',
            departmentHeroDesc: 'Oral AI背后的杰出人才，致力于通过协作和创新革新牙科诊断。',
            systems: '系统',
            backendDesign: '后端设计',
            backendDeveloper: '后端开发人员',
            backendDevDesc: '构建健壮的API并管理高性能模型推理引擎。',
            uiux: 'UI/UX',
            frontendDesign: '前端设计',
            frontendDeveloper: '前端开发人员',
            frontendDevDesc: '打造直观且响应式的用户界面，实现无缝医疗分析。',
            dataTeam: '数据团队',
            datasetAnnotation: '数据集标注与准备',
            datasetAnnotationDesc: '确保为我们的AI模型提供最高质量的训练数据。',
            datasetSpecialist: '数据集专家',
            datasetSpecialistDesc1: '医学图像标注和数据预处理管道专家。',
            datasetSpecialistDesc2: '专注于数据质量保证和数据集平衡技术。',
            datasetSpecialistDesc3: '专注于病理特征提取和元数据管理。',
            
            // Blog Page
            oralAiJournal: 'Oral AI期刊',
            blogHeroTitle: '洞察、更新与故事',
            blogHeroDesc: '深入了解我们的技术、患者健康指南以及AI在牙科领域的未来。',
            engineering: '工程',
            featuredPostTitle: '准确性架构：深入了解Oral AI的双模型系统',
            featuredPostDesc: '我们如何将分诊路由器与专业的临床和组织病理学模型相结合，实现99.8%的诊断精度。',
            readArticle: '阅读文章',
            ourBlog: '我们的博客',
            latestArticles: '最新文章',
            patientHealth: '患者健康',
            blogPost1Title: '不容忽视的5个口腔健康问题早期迹象',
            blogPost1Desc: '从细微的变色到轻微的敏感，了解您的口腔在问题变大之前试图告诉您什么。',
            behindTheScenes: '幕后花絮',
            blogPost2Title: '从数据到诊断：我们如何构建数据集',
            blogPost2Desc: '了解我们数据集团队使用的严格策展过程，以确保我们的AI从最高质量的医学图像中学习。',
            futureTech: '未来技术',
            blogPost3Title: '远程牙科的未来：AI作为第一响应者',
            blogPost3Desc: '想象一下通过智能手机获得初步诊断。这就是Oral AI如何使远程筛查成为现实。',
            
            // News/Pages Page
            industryInsights: '行业洞察',
            eraOfMedicalAi: '医疗AI时代',
            pagesHeroDesc: '探索人工智能如何重塑医疗健康领域，从早期诊断到个性化治疗方案。',
            diagnostics: '诊断',
            newsArticle1Title: 'AI在早期癌症检测中超越人类专家',
            newsArticle1Desc: '最近的研究显示，深度学习模型在识别医学影像中的早期异常方面达到了99%的准确率，显著减少了假阴性。',
            readFullStory: '阅读完整故事',
            robotics: '机器人技术',
            newsArticle2Title: '精准手术：AI辅助手术的崛起',
            newsArticle2Desc: '外科医生现在正在利用AI驱动的机器人手臂以亚毫米级精度执行复杂手术，最大限度地减少患者的恢复时间。',
            pharma: '制药',
            newsArticle3Title: '加速药物发现',
            newsArticle3Desc: '生成式AI通过预测分子相互作用，正在将药物开发时间从数年缩短到数月。',
            genomics: '基因组学',
            newsArticle4Title: '超个性化医学',
            newsArticle4Desc: 'AI算法分析基因组数据，现在可以根据个人的DNA档案专门定制治疗方案。',
            patientCare: '患者护理',
            newsArticle5Title: '24/7虚拟健康助手',
            newsArticle5Desc: 'LLM驱动的聊天机器人正在全球范围内提供即时、准确的医疗分诊和心理健康支持。',
            joinTheRevolution: '加入革命',
            joinRevolutionDesc: 'Oral AI处于这一变革的最前沿。今天就体验我们的尖端诊断工具。',
            tryOralAiNow: '立即试用Oral AI',
            
            // CTA Section
            trustedHealthcare: '值得信赖的医疗保健',
            empoweringEarlyDetection: '赋能早期检测<br>拯救生命。',
            joinThousandsDesc: '加入数千名信任Oral AI的患者和临床医生，进行快速、准确、便捷的口腔健康筛查。',
            accuracyRate: '准确率',
            patientsScreened: '已筛查患者',
            aiAvailability: 'AI可用性',
            supportLabel: '支持',
            needExpertAdvice: '需要专家建议？',
            medicalTeamHelp: '我们的医疗团队随时帮助您解读结果并指导下一步行动。',
            callUsNow: '立即致电',
            emailSupport: '邮件支持',
            
            // Testimonials
            testimonialsLabel: '用户评价',
            whatPatientsSay: '患者怎么说',
            testimonialsDesc: '来自使用我们AI筛查工具进行早期检测和安心的人们的真实故事。',
            testimonial1: '"AI筛查速度非常快。我担心牙龈上的一个斑点，这个工具给了我即时评估，帮助我决定去看医生。"',
            testimonial2: '"作为吸烟者，我担心口腔健康。这个应用帮助我追踪变化。报告生成非常专业且易于理解。"',
            testimonial3: '"我向患者推荐这个用于就诊间的自我监测。病变检测的准确性令人印象深刻且可靠。"',
            testimonial4: '"界面非常容易使用。我只是上传了一张照片，几秒钟内就得到了结果。在我最需要的时候给了我安心。"',
            testimonial5: '"对于教育目的也是一个很棒的工具。它帮助可视化不同口腔状况的外观。对学生非常有帮助。"',
            testimonial6: '"我担心一个不愈合的溃疡。应用建议我去看专家，我很高兴我这样做了。早期检测有效。"',
            rolePatient: '患者',
            roleRegularUser: '普通用户',
            roleDentalHygienist: '牙科卫生师',
            roleStudent: '学生',
            roleDoctor: '医生',
            roleAdmin: '管理员',
            
            // Notifications
            notificationsTitle: '通知',
            markAllRead: '全部标为已读',
            noNewNotifications: '没有新通知',
            allCaughtUp: '全部看完了！',
            noNewNotificationsOrAppointments: '没有新通知或预约。',
            
            // Model B Results
            qualityNoteLowRes: '低分辨率。已切换到标准模式以获得更好的稳定性。',
            screeningResultNormal: '正常',
            screeningResultRefertoDentist: '建议就医',
            hygieneScoreHigh: '高',
            hygieneScoreMedium: '中',
            hygieneScoreLow: '低',
            noIssuesDetected: '未检测到特定问题。',
            detectedCount: '检测到{count}个',
            conditionCaries: '龋齿',
            conditionGingivitis: '牙龈炎',
            conditionUlcer: '溃疡',
            conditionTooth: '牙齿',
            conditionCalculus: '牙结石',
            conditionHypodontia: '先天缺牙',
            
            // Model A Results
            tumourDetected: '检测到肿瘤',
            noTumour: '无肿瘤',
            detected: '已检测',
            notDetected: '未检测到',
            
            // Technology Modal
            techPytorchSubtitle: '深度学习框架',
            techPytorchBeginner: "PyTorch由Facebook开发，是另一个广泛用于构建神经网络的深度学习框架。其简单的Python风格使初学者易于掌握模型创建和训练的基础知识。初学者会欣赏PyTorch在创建图像分类简单模型方面的灵活性，无需担心过多的技术开销。",
            techPytorchAdvanced: "高级用户可以使用PyTorch的动态计算图，在构建复杂架构、自定义损失函数和优化器时具有更大的灵活性。对于研究人员来说，这是一个很好的选择，因为PyTorch提供了与视觉语言模型、生成对抗网络（GAN）和深度强化学习等前沿模型的无缝实验。由于其高效的内存管理和GPU支持，它在处理大型数据集方面也表现出色。",
            techCudaSubtitle: 'GPU加速',
            techCudaBeginner: "CUDA是NVIDIA开发的并行计算平台和编程模型，而cuDNN是用于深度神经网络的GPU加速库。对于初学者来说，这些工具可能看起来很技术性，但它们的主要目的是通过利用GPU能力来加速深度学习模型的训练。通过在训练环境中正确设置CUDA和cuDNN，可以显著提高模型训练的速度和优化，特别是在使用TensorFlow和PyTorch等框架时。",
            techCudaAdvanced: "专家可以利用CUDA和cuDNN的全部功能来优化高需求应用程序的性能。这包括为特定操作编写自定义CUDA内核、高效管理GPU内存以及微调神经网络训练以获得最大速度和可扩展性。这些工具对于处理大型数据集并需要从模型中获得顶级性能的开发人员至关重要。",
            techYoloSubtitle: '实时目标检测',
            techYoloBeginner: "YOLO（You Only Look Once）是一种快速目标检测算法，特别适用于实时应用。初学者可以使用预训练的YOLO模型，通过相对简单的代码快速检测图像或视频中的物体。易用性使YOLO成为那些想要探索目标检测而无需从头构建复杂模型的人的绝佳切入点。",
            techYoloAdvanced: "YOLO提供了在自定义数据集上微调模型以检测特定物体的机会，提高检测速度和准确性。YOLO的轻量级特性使其可以部署在资源受限的环境中，如移动设备，使其成为实时应用的首选解决方案。专业人员还可以尝试新版本的YOLO，调整参数以满足特定项目需求。"
        },
        ta: {
            // Navigation
            home: 'முகப்பு',
            about: 'பற்றி',
            services: 'சேவைகள்',
            department: 'துறை',
            news: 'செய்திகள்',
            blog: 'வலைப்பதிவு',
            contact: 'தொடர்பு',
            login: 'உள்நுழைய',
            signUp: 'பதிவு செய்ய',
            logout: 'வெளியேறு',
            myProfile: 'என் சுயவிவரம்',
            settings: 'அமைப்புகள்',
            
            // Common Buttons & Actions
            save: 'சேமி',
            saveChanges: 'மாற்றங்களைச் சேமிக்கவும்',
            cancel: 'ரத்து',
            close: 'மூடு',
            submit: 'சமர்ப்பி',
            delete: 'நீக்கு',
            edit: 'திருத்து',
            search: 'தேடு',
            loading: 'ஏற்றுகிறது...',
            updating: 'புதுப்பிக்கிறது...',
            change: 'மாற்று',
            viewMore: 'மேலும் பார்க்க',
            learnMore: 'மேலும் அறிய',
            getStarted: 'தொடங்கு',
            bookAppointment: 'சந்திப்பை பதிவு செய்',
            discoverMore: 'மேலும் அறிய',
            startScreening: 'தரப்படுத்தலை தொடங்கு',
            tryNow: 'இப்போது முயற்சிக்கவும்',
            
            // Home Page Hero
            welcomeTitle: 'AI-இயங்கும் சந்திப்பு & நோய் கண்டறிதல்',
            welcomeSubtitle: 'நோயாளி சந்திப்புகளை செயலற்ற முறையில் நிர்வகிக்கவும், அதிநவீன AI பயன்படுத்தி வாய்புரவு புற்றுநோயை செய்யவும், தொழில்முறை தர பகுப்பாய்வு மேற்கொள்ளவும்.',
            advancedOralHealth: 'மேம்பட்ட வாய் சுகாதாரம்',
            viewCalendar: 'நாள்காட்டியைப் பார்',
            accuracyRate: 'துல்லிய விகிதம்',
            analysisTime: 'பகுப்பாய்வு நேரம்',
            compliant: 'இணக்கமான',
            
            // New Hero Section
            trustedBy: '10,000+ சுகாதார நிபுணர்களால் நம்பப்படுகிறது',
            heroLine1: 'அடுத்த தலைமுறை',
            heroLine2: 'வாய் சுகாதார AI',
            heroLine3: 'தளம்',
            accuracy: 'துல்லியம்',
            results: 'முடிவுகள்',
            secure: 'பாதுகாப்பான',
            readyToScan: 'ஸ்கேன் செய்ய தயார்',
            detection: 'கண்டறிதல்',
            speed: 'வேகம்',
            aiModels: 'AI மாடல்கள்',
            noIssues: 'பிரச்சினைகள்',
            detected: 'கண்டறியப்படவில்லை',
            aiPowered: 'AI இயக்கப்படும்',
            analysis: 'பகுப்பாய்வு',
            scrollToExplore: 'ஆராய உருட்டவும்',
            
            // Quick Actions (New)
            quickAccess: 'விரைவு அணுகல்',
            whatToDo: 'இன்று நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?',
            aiScreening: 'AI திரையிடல்',
            analyzeImages: 'படங்களை பகுப்பாய்வு செய்',
            scheduleVisit: 'வருகையை திட்டமிடு',
            manageSchedule: 'அட்டவணையை நிர்வகி',
            getHelp: 'உதவி பெறு',
            talkToExpert: 'நிபுணரிடம் பேசு',
            
            // Quick Actions
            aiAnalysis: 'AI பகுப்பாய்வு',
            scheduleMeeting: 'கூட்டத்தை திட்டமிடு',
            viewReports: 'அறிக்கைகளைப் பார்',
            analysisHistory: 'பகுப்பாய்வு வரலாறு',
            contactDoctor: 'மருத்துவரை தொடர்பு கொள்',
            getSupport: 'ஆதரவைப் பெறு',
            
            // Calendar Section
            appointmentCalendar: 'சந்திப்பு நாள்காட்டி',
            calendarDesc: 'உங்கள் சந்திப்புகளைப் பார்க்கவும் நிர்வகிக்கவும். விவரங்களைப் பார்க்க அல்லது புதிய சந்திப்பை பதிவு செய்ய எந்த தேதியையும் கிளிக் செய்யுங்கள்.',
            loginToViewAppointments: 'உங்கள் சந்திப்புகளைப் பார்க்க உள்நுழையுங்கள்',
            upcomingAppointments: 'வரவிருக்கும் சந்திப்புகள்',
            legend: 'குறியீடு',
            colorGuide: 'வண்ண வழிகாட்டி',
            patientAppointments: 'நோயாளி சந்திப்புகள்',
            
            // Status & Feedback
            error: 'பிழை',
            success: 'வெற்றி',
            warning: 'எச்சரிக்கை',
            info: 'தகவல்',
            
            // Profile & Settings
            fullName: 'முழு பெயர்',
            emailAddress: 'மின்னஞ்சல் முகவரி',
            password: 'கடவுச்சொல்',
            currentPassword: 'தற்போதைய கடவுச்சொல்',
            newPassword: 'புதிய கடவுச்சொல்',
            confirmPassword: 'புதிய கடவுச்சொல்லை உறுதிப்படுத்தவும்',
            changePassword: 'கடவுச்சொல்லை மாற்று',
            updatePassword: 'கடவுச்சொல்லை புதுப்பிக்கவும்',
            enterCurrentPassword: 'தற்போதைய கடவுச்சொல்லை உள்ளிடவும்',
            enterNewPassword: 'புதிய கடவுச்சொல்லை உள்ளிடவும்',
            confirmNewPassword: 'புதிய கடவுச்சொல்லை உறுதிப்படுத்தவும்',
            emailCannotChange: 'பாதுகாப்பான முறையில் மின்னஞ்சலை மாற்ற முடியாது.',
            changeYourPassword: 'உங்கள் கணக்கு கடவுச்சொல்லை மாற்றவும்',
            lastChanged: 'கடைசியாக மாற்றப்பட்டது',
            
            // Settings Page
            general: 'பொதுவான',
            security: 'பாதுகாப்பு',
            patientManagement: 'நோயாளி மேலாண்மை',
            generalPreferences: 'பொதுவான விருப்பத்தேர்வுகள்',
            securitySettings: 'பாதுகாப்பு அமைப்புகள்',
            languageRegion: 'மொழி மற்றும் பிராந்தியம்',
            preferredLanguage: 'விருப்பமான மொழி',
            selectLanguage: 'இடைமுகத்திற்கான உங்கள் விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்',
            reportSettings: 'அறிக்கை அமைப்புகள்',
            autoSaveReports: 'தானாக சேமிப்பு அறிக்கைகள்',
            autoSaveDesc: 'பகுப்பாய்வு அறிக்கைகளை உங்கள் கணக்கில் தானாகச் சேமிக்கவும்',
            notifications: 'அறிவிப்புகள்',
            emailNotifications: 'மின்னஞ்சல் அறிவிப்புகள்',
            emailNotifDesc: 'சந்திப்புகள் பற்றிய புதுப்பிப்புகளைப் பெறுங்கள்',
            passwordChangeInfo: 'கடவுச்சொல் மாற்றங்களுக்கு மீண்டும் அங்கீகாரம் தேவை.',
            
            // Home Page
            welcomeTitle: 'AI-இயங்கும் வாய் சுகாதார பகுப்பாய்வு',
            welcomeSubtitle: 'அதிநவீன கணினி பார்வையைப் பயன்படுத்தி மேம்பட்ட நோய் கண்டறிதல்',
            advancedAI: 'மேம்பட்ட AI',
            accurateResults: 'துல்லியமான முடிவுகள்',
            fastAnalysis: 'விரைவான பகுப்பாய்வு',
            getAnalysis: 'பகுப்பாய்வு பெறுக',
            
            // Messages
            passwordUpdated: 'கடவுச்சொல் வெற்றிகரமாக புதுப்பிக்கப்பட்டது! உங்கள் கணக்கு இப்போது மிகவும் பாதுகாப்பானது.',
            passwordMismatch: 'புதிய கடவுச்சொற்கள் பொருந்தவில்லை! மீண்டும் முயற்சிக்கவும்.',
            passwordTooShort: 'புதிய கடவுச்சொல் குறைந்தது 6 எழுத்துக்கள் நீளமாக இருக்க வேண்டும்.',
            networkError: 'நெட்வொர்க் பிழை. உங்கள் இணைப்பைச் சரிபார்த்து மீண்டும் முயற்சிக்கவும்.',
            languageChanged: 'மொழி வெற்றிகரமாக மாற்றப்பட்டது. இடைமுகம் புதுப்பிக்கப்பட்டது!',
            autoSaveEnabled: 'தானாக சேமிப்பு இயக்கப்பட்டது. உங்கள் அறிக்கைகள் தானாக சேமிக்கப்படும்.',
            autoSaveDisabled: 'தானாக சேமிப்பு முடக்கப்பட்டது. நீங்கள் அறிக்கைகளை கைமுறையாக சேமிக்க வேண்டும்.',
            emailNotifEnabled: 'மின்னஞ்சல் அறிவிப்புகள் இயக்கப்பட்டன. சந்திப்பு புதுப்பிப்புகளைப் பெறுவீர்கள்.',
            emailNotifDisabled: 'மின்னஞ்சல் அறிவிப்புகள் முடக்கப்பட்டன. நீங்கள் சந்திப்பு மின்னஞ்சல்களைப் பெற மாட்டீர்கள்.',
            profileUpdated: 'சுயவிவரம் வெற்றிகரமாக புதுப்பிக்கப்பட்டது!',
            pleaseEnterName: 'செல்லுபடியாகும் பெயரை உள்ளிடவும்',
            appointmentBooked: 'சந்திப்பு பதிவு செய்யப்பட்டது!',
            pleaseSelectTime: 'நேரத்தை தேர்ந்தெடுக்கவும்',
            failedToBook: 'பதிவு தோல்வியடைந்தது',
            sessionExpired: 'அமர்வு காலாவதியானது',
            
            // Footer
            quickLinks: 'விரைவு இணைப்புகள்',
            resources: 'ஆதாரங்கள்',
            legal: 'சட்ட',
            privacyPolicy: 'தனியுரிமை கொள்கை',
            termsOfService: 'சேவை விதிமுறைகள்',
            cookiePolicy: 'குக்கீ கொள்கை',
            hipaaCompliance: 'HIPAA இணக்கம்',
            followUs: 'எங்களைப் பின்தொடரவும்',
            allRightsReserved: 'அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை',
            platform: 'தளம்',
            aboutUs: 'எங்களை பற்றி',
            ourTeams: 'எங்கள் அணிகள்',
            tryAITool: 'AI கருவியை முயற்சிக்கவும்',
            stayUpdated: 'புதுப்பிப்புகளைப் பெறுங்கள்',
            newsletterDesc: 'சமீபத்திய AI மருத்துவ முன்னேற்றங்களுக்கு எங்கள் செய்திமடலுக்கு குழுசேரவும்.',
            enterYourEmail: 'உங்கள் மின்னஞ்சலை உள்ளிடவும்',
            join: 'சேர்',
            designedForHealthcare: 'சிறந்த சுகாதாரத்திற்காக வடிவமைக்கப்பட்டது.',
            footerTagline: 'மேம்பட்ட AI தொழில்நுட்பத்துடன் பல் நோயறிதலின் எதிர்காலத்தை முன்னெடுக்கிறோம்.',
            
            // Additional Settings
            managePersonalInfo: 'உங்கள் தனிப்பட்ட தகவலை நிர்வகிக்கவும்',
            patientRecords: 'நோயாளி பதிவுகள்',
            managePatients: 'பதிவுசெய்யப்பட்ட நோயாளிகளையும் அவர்களின் கணக்குகளையும் நிர்வகிக்கவும்.',
            searchPatients: 'பெயர் அல்லது மின்னஞ்சல் மூலம் நோயாளிகளைத் தேடுங்கள்...',
            loadingRecords: 'பதிவுகளை ஏற்றுகிறது...',
            id: 'அடையாளம்',
            email: 'மின்னஞ்சல்',
            status: 'நிலை',
            actions: 'செயல்கள்',
            schedule: 'அட்டவணை',
            refresh: 'புதுப்பி',
            confirm: 'உறுதிப்படுத்து',
            confirmBooking: 'பதிவை உறுதிப்படுத்து',
            or: 'அல்லது',
            guest: 'விருந்தினர்',
            doctorView: 'மருத்துவர் பார்வை',
            patientView: 'நோயாளி பார்வை',
            month: 'மாதம்',
            week: 'வாரம்',
            verified: 'சரிபார்க்கப்பட்டது',
            helpful: 'உதவிகரமானது',
            pending: 'நிலுவையில்',
            confirmed: 'உறுதிசெய்யப்பட்டது',
            
            // Calendar & Booking
            dailySchedule: 'தினசரி அட்டவணை',
            selectDate: 'தேதியை தேர்ந்தெடுக்கவும்',
            noAppointments: 'சந்திப்புகள் திட்டமிடப்படவில்லை',
            enjoyFreeTime: 'உங்கள் ஓய்வு நேரத்தை அனுபவியுங்கள், மருத்துவரே.',
            doctor: 'மருத்துவர்',
            time: 'நேரம்',
            dateTime: 'தேதி மற்றும் நேரம்',
            notes: 'குறிப்புகள்',
            noNotesProvided: 'குறிப்புகள் வழங்கப்படவில்லை',
            yourAppointments: 'உங்கள் சந்திப்புகள்',
            editAppointment: 'சந்திப்பை திருத்து',
            saveChanges: 'மாற்றங்களை சேமி',
            
            // Guest Modal
            welcome: 'வரவேற்கிறோம்!',
            needAccountToManage: 'சந்திப்புகளை நிர்வகிக்க உங்களுக்கு ஒரு கணக்கு தேவை.',
            logIn: 'உள்நுழை',
            createAccount: 'கணக்கை உருவாக்கு',
            
            // Login Page
            signIn: 'உள்நுழை',
            signInTitle: 'உள்நுழைவு',
            enterCredentials: 'உங்கள் கணக்கை அணுக உங்கள் சான்றுகளை உள்ளிடவும்',
            rememberMe: 'என்னை நினைவில் கொள்',
            forgotPassword: 'கடவுச்சொல் மறந்துவிட்டதா?',
            signingIn: 'உள்நுழைகிறது...',
            dontHaveAccount: 'கணக்கு இல்லையா?',
            welcomeBack: 'மீண்டும் வரவேற்கிறோம்.',
            loginDesc: 'சந்திப்புகளை நிர்வகிக்கவும், பகுப்பாய்வு அறிக்கைகளைப் பார்க்கவும், மருத்துவ நிபுணர்களுடன் இணைக்கவும் உங்கள் தனிப்பயன் டாஷ்போர்டை அணுகவும்.',
            accuracyRate: 'துல்லிய விகிதம்',
            aiAvailability: 'AI கிடைக்கும்',
            
            // Register Page
            joinUsToday: 'இன்றே எங்களுடன் சேருங்கள்.',
            registerDesc: 'அதிநவீன AI வாய் திரையிடல் அணுக, நிபுணர்களுடன் சந்திப்புகளை நிர்வகிக்க, உங்கள் வாய் சுகாதார பயணத்தைக் கண்காணிக்க கணக்கை உருவாக்குங்கள்.',
            freeInitialScreening: 'இலவச ஆரம்ப AI திரையிடல்',
            secureMedicalRecords: 'பாதுகாப்பான மருத்துவ பதிவுகள்',
            directSpecialistBooking: 'நேரடி நிபுணர் பதிவு',
            fillDetails: 'தொடங்க உங்கள் விவரங்களை நிரப்புங்கள்',
            iAmA: 'நான் ஒரு...',
            patientRole: 'நோயாளி (என் ஆரோக்கியத்தை சோதிக்க விரும்புகிறேன்)',
            doctorRole: 'மருத்துவ நிபுணர் (சிகிச்சை அளிக்க விரும்புகிறேன்)',
            creatingAccount: 'கணக்கை உருவாக்குகிறது...',
            alreadyHaveAccount: 'ஏற்கனவே கணக்கு உள்ளதா?',
            bySigningUp: 'பதிவு செய்வதன் மூலம், நீங்கள் எங்கள் விதிமுறைகளை ஏற்கிறீர்கள்',
            terms: 'விதிமுறைகள்',
            and: '&',
            
            // Why Choose Section
            whyChooseTitle: 'ஏன் Oral AI-ஐ தேர்வு செய்ய வேண்டும்?',
            whyChooseHeading: 'மருத்துவ நிபுணத்துவத்தை செயற்கை நுண்ணறிவுடன் இணைக்கிறோம்',
            whyChooseDesc: 'முன்னெப்போதையும் விட வேகமாகவும் துல்லியமாகவும் அசாதாரணங்களைக் கண்டறியும் இரண்டாவது கருத்து AI கருவிகளுடன் பல் நிபுணர்களை நாங்கள் வலுப்படுத்துகிறோம்.',
            instantResults: 'உடனடி முடிவுகள்',
            instantResultsDesc: 'நிகழ்நேர பகுப்பாய்வு',
            highPrecision: 'உயர் துல்லியம்',
            highPrecisionDesc: 'நுண்ணிய விவரம்',
            secureData: 'பாதுகாப்பான தரவு',
            secureDataDesc: 'HIPAA இணக்கம்',
            expertSupport: 'நிபுணர் ஆதரவு',
            expertSupportDesc: 'மருத்துவர்களால் சரிபார்க்கப்பட்டது',
            
            // Services Section
            ourServices: 'எங்கள் சேவைகள்',
            comprehensiveAnalysis: 'விரிவான AI பகுப்பாய்வு',
            comprehensiveAnalysisDesc: 'எங்கள் பல-மாதிரி கட்டமைப்பு ஒவ்வொரு வழக்கும் அந்த குறிப்பிட்ட முறைமைக்கு வடிவமைக்கப்பட்ட நிபுணர் அல்காரிதத்தால் கையாளப்படுவதை உறுதி செய்கிறது.',
            smartTriage: 'புத்திசாலி டிரியேஜ்',
            tryTriage: 'டிரியேஜை முயற்சிக்கவும்',
            histopathology: 'ஹிஸ்டோபத்தாலஜி',
            analyzeSlide: 'ஸ்லைடை பகுப்பாய்வு செய்',
            clinicalScreening: 'மருத்துவ திரையிடல்',
            
            // CTA Section
            trustedHealthcare: 'நம்பகமான சுகாதாரம்',
            empoweringDetection: 'ஆரம்ப கண்டறிதலை வலுப்படுத்தி உயிர்களைக் காப்பாற்றுகிறோம்.',
            empoweringDesc: 'விரைவான, துல்லியமான மற்றும் அணுகக்கூடிய வாய் சுகாதார திரையிடலுக்கு Oral AI-ஐ நம்பும் ஆயிரக்கணக்கான நோயாளிகள் மற்றும் மருத்துவர்களுடன் சேருங்கள்.',
            patientsScreened: 'திரையிடப்பட்ட நோயாளிகள்',
            needExpertAdvice: 'நிபுணர் ஆலோசனை தேவையா?',
            expertAdviceDesc: 'உங்கள் முடிவுகளை விளக்கவும் அடுத்த படிகளை வழிநடத்தவும் எங்கள் மருத்துவ குழு இங்கே உள்ளது.',
            callUsNow: 'இப்போது எங்களை அழைக்கவும்',
            emailSupport: 'மின்னஞ்சல் ஆதரவு',
            
            // Testimonials
            testimonials: 'சாட்சியங்கள்',
            whatPatientsSay: 'எங்கள் நோயாளிகள் என்ன சொல்கிறார்கள்',
            realStories: 'ஆரம்ப கண்டறிதல் மற்றும் மன அமைதிக்காக எங்கள் AI திரையிடல் கருவியைப் பயன்படுத்திய மக்களின் உண்மையான கதைகள்.',
            patient: 'நோயாளி',
            regularUser: 'வழக்கமான பயனர்',
            dentalHygienist: 'பல் சுகாதார நிபுணர்',
            
            // Triage/Analysis Page
            aiPoweredDiagnostics: 'AI-இயங்கும் நோயறிதல்',
            intelligentAnalysis: 'புத்திசாலி வாய் நோய் பகுப்பாய்வு',
            triageDesc: 'மருத்துவ படங்களையும் ஹிஸ்டோபத்தாலஜி ஸ்லைடுகளையும் துல்லியமாக வகைப்படுத்த அதிநவீன AI-ஐ பயன்படுத்துகிறது.',
            dropImageHere: 'உங்கள் படத்தை இங்கே விடுங்கள், அல்லது உலாவ கிளிக் செய்யுங்கள்',
            supportsFormats: 'JPG, JPEG, PNG ஆதரிக்கப்படுகிறது (மருத்துவ அல்லது ஹிஸ்டோபத்தாலஜி)',
            secureUpload: 'பாதுகாப்பான & தனிப்பட்ட பதிவேற்றம்',
            analyzingImage: 'பட அமைப்பை பகுப்பாய்வு செய்கிறது...',
            routingToModel: 'பொருத்தமான நிபுணர் மாதிரிக்கு அனுப்புகிறது',
            systemCapabilities: 'அமைப்பு திறன்கள்',
            autoRouting: 'தானியங்கு திசைவு',
            deepLearning: 'ஆழ் கற்றல்',
            objectDetection: 'பொருள் கண்டறிதல்',
            
            // Model A
            histopathologyAnalysis: 'ஹிஸ்டோபத்தாலஜி பகுப்பாய்வு',
            aiAnalysisInsight: 'AI பகுப்பாய்வு நுண்ணறிவு',
            loadingSuggestion: 'பரிந்துரையை ஏற்றுகிறது...',
            primaryDiagnosis: 'முதன்மை நோயறிதல்',
            analyzing: 'பகுப்பாய்வு செய்கிறது...',
            confidence: 'நம்பிக்கை',
            microscopicFeatures: 'நுண்ணோக்கி அம்சங்கள்',
            depthOfInvasion: 'ஊடுருவல் ஆழம்',
            original: 'அசல்',
            heatmap: 'வெப்ப வரைபடம்',
            heatmapInfo: 'வெப்ப வரைபடங்கள் அதிக நிகழ்தகவு கட்டி பகுதிகளை காட்சிப்படுத்துகின்றன.',
            
            // Model B
            clinicalAnalysis: 'மருத்துவ பகுப்பாய்வு',
            detectedConditions: 'கண்டறியப்பட்ட நிலைமைகள்',
            noConditionsDetected: 'நிலைமைகள் கண்டறியப்படவில்லை',
            
            // Chat Widget
            aiAssistant: 'AI உதவியாளர்',
            onlineStatus: 'ஆன்லைன் - உதவ தயார்',
            askAnything: 'வாய் சுகாதாரம் பற்றி எதையும் கேளுங்கள்...',
            typeMessage: 'உங்கள் செய்தியை தட்டச்சு செய்யுங்கள்...',
            send: 'அனுப்பு',
            clearChat: 'அரட்டையை அழி',
            
            // About Page
            whoWeAre: 'நாங்கள் யார்',
            aboutOralAI: 'Oral AI பற்றி',
            aboutDesc: 'மருத்துவ நிபுணத்துவம் மற்றும் மேம்பட்ட செயற்கை நுண்ணறிவின் இணைவு மூலம் பல் நோயறிதலின் எதிர்காலத்தை முன்னெடுக்கிறோம்.',
            ourMission: 'எங்கள் நோக்கம்',
            democratizingHealthcare: 'மேம்பட்ட வாய் சுகாதாரத்தை ஜனநாயகமாக்குதல்',
            missionDesc: 'அனைவருக்கும் உயர்தர வாய் நோய் கண்டறிதலை அணுகக்கூடியதாக மாற்றுவதே எங்கள் நோக்கம்.',
            analysisAccuracy: 'பகுப்பாய்வு துல்லியம்',
            systemAvailability: 'அமைப்பு கிடைக்கும்',
            ourCoreValues: 'எங்கள் அடிப்படை மதிப்புகள்',
            whatDrivesUs: 'எங்களை இயக்குவது என்ன',
            patientFirst: 'நோயாளி முதலில்',
            patientFirstDesc: 'நாங்கள் உருவாக்கும் ஒவ்வொரு அல்காரிதமும் நோயாளி பராமரிப்பு மற்றும் பாதுகாப்பை மேம்படுத்தும் இலக்கோடு வடிவமைக்கப்பட்டுள்ளது.',
            scientificRigor: 'அறிவியல் கடுமை',
            scientificRigorDesc: 'நாங்கள் அறிவியல் சரிபார்ப்பின் உயர்ந்த தரங்களைப் பின்பற்றுகிறோம்.',
            dataPrivacy: 'தரவு தனியுரிமை',
            dataPrivacyDesc: 'நாங்கள் நோயாளி தரவை மிக உயர்ந்த மரியாதை மற்றும் பாதுகாப்புடன் நடத்துகிறோம்.',
            ourTechnology: 'எங்கள் தொழில்நுட்பம்',
            poweredByInnovation: 'புதுமையால் இயக்கப்படுகிறது',
            techDesc: 'எங்கள் AI-க்கு பின்னால் உள்ள அதிநவீன கருவிகளை ஆராய கீழே உள்ள அட்டைகளை கிளிக் செய்யுங்கள்.',
            deepLearningFramework: 'ஆழ் கற்றல் கட்டமைப்பு',
            explore: 'ஆராயுங்கள்',
            
            // Contact Page
            getInTouch: 'தொடர்பு கொள்ளுங்கள்',
            hereToHelp: 'உதவ இங்கே இருக்கிறோம்',
            contactDesc: 'எங்கள் AI தொழில்நுட்பம் பற்றி கேள்விகள் உள்ளதா அல்லது ஆதரவு தேவையா? எங்கள் குழுவை தொடர்பு கொள்ளுங்கள்.',
            contactInformation: 'தொடர்பு தகவல்',
            teamAvailable: 'எங்கள் குழு திங்கள் முதல் வெள்ளி வரை உங்களுக்கு உதவ கிடைக்கும்.',
            emailUs: 'மின்னஞ்சல் அனுப்புங்கள்',
            callUs: 'எங்களை அழையுங்கள்',
            visitUs: 'எங்களை பாருங்கள்',
            sendMessage: 'செய்தி அனுப்புங்கள்',
            subject: 'பொருள்',
            message: 'செய்தி',
            generalInquiry: 'பொது விசாரணை',
            technicalSupport: 'தொழில்நுட்ப ஆதரவு',
            partnershipOpportunity: 'கூட்டாண்மை வாய்ப்பு',
            pressMedia: 'செய்தி & ஊடகம்',
            howCanWeHelp: 'நாங்கள் எவ்வாறு உதவ முடியும்?',
            supportCenter: 'ஆதரவு மையம்',
            faq: 'அடிக்கடி கேட்கப்படும் கேள்விகள்',
            faqDesc: 'Oral AI தொழில்நுட்பம் மற்றும் சேவைகள் பற்றி நீங்கள் தெரிந்து கொள்ள வேண்டிய அனைத்தும்.',
            
            // Additional Login/Register
            loginBrandingDesc: 'சந்திப்புகளை நிர்வகிக்கவும், பகுப்பாய்வு அறிக்கைகளைப் பார்க்கவும், மருத்துவ நிபுணர்களுடன் தடையின்றி இணைக்கவும் உங்கள் தனிப்பயன் டாஷ்போர்டை அணுகவும்.',
            registerBrandingDesc: 'அதிநவீன AI வாய் திரையிடல் அணுக, நிபுணர்களுடன் சந்திப்புகள் பதிவு செய்ய, உங்கள் வாய் சுகாதார பயணத்தைக் கண்காணிக்க கணக்கை உருவாக்கவும்.',
            fillInDetails: 'தொடங்க உங்கள் விவரங்களை நிரப்பவும்',
            rolePatient: 'நோயாளி (என் ஆரோக்கியத்தை சோதிக்க விரும்புகிறேன்)',
            roleDoctor: 'மருத்துவ நிபுணர் (சிகிச்சை அளிக்க விரும்புகிறேன்)',
            fullNamePlaceholder: 'ராஜா குமார்',
            emailPlaceholder: 'name@example.com',
            copyrightText: '© 2026 Oral AI தளம். அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.',
            appName: 'Oral AI',
            
            // About Page Additional
            aboutHeroDesc: 'மருத்துவ நிபுணத்துவம் மற்றும் மேம்பட்ட செயற்கை நுண்ணறிவின் கலவையுடன் பல் நோயறிதலின் எதிர்காலத்தை முன்னெடுக்கிறோம்.',
            techSectionDesc: 'எங்கள் AI-க்கு பின்னால் உள்ள அதிநவீன கருவிகளை ஆராய கீழே உள்ள அட்டைகளை கிளிக் செய்யவும்.',
            gpuAcceleration: 'GPU முடுக்கம்',
            realTimeObjectDetection: 'நிகழ்நேர பொருள் கண்டறிதல்',
            beginner: 'ஆரம்பம்',
            advanced: 'மேம்பட்ட',
            
            // Contact Page Additional
            contactHeroDesc: 'எங்கள் AI தொழில்நுட்பம் பற்றி கேள்விகள் உள்ளதா அல்லது ஆதரவு தேவையா? எங்கள் குழுவை தொடர்பு கொள்ளுங்கள்.',
            teamAvailability: 'எங்கள் குழு திங்கள் முதல் வெள்ளி வரை எந்த விசாரணைக்கும் உங்களுக்கு கிடைக்கும்.',
            businessHours: 'திங்கள்-வெள்ளி, காலை 9 மணி - மாலை 6 மணி',
            sendUsMessage: 'எங்களுக்கு செய்தி அனுப்புங்கள்',
            messagePlaceholder: 'நாங்கள் எவ்வாறு உதவ முடியும்?',
            faqAccuracyQuestion: 'AI நோயறிதல் எவ்வளவு துல்லியமானது?',
            faqAccuracyAnswer: 'எங்கள் இரட்டை-மாதிரி அமைப்பு மருத்துவ சோதனைகளில் <strong>99.9% துல்லியத்தை</strong> அடைந்துள்ளது. இருப்பினும், இது ஒரு திரையிடல் கருவியாக வடிவமைக்கப்பட்டுள்ளது மற்றும் தொழில்முறை பல் பரிசோதனையை மாற்றக்கூடாது. ஆரம்ப கண்டறிதல் மற்றும் கண்காணிப்புக்கு இதைப் பயன்படுத்த பரிந்துரைக்கிறோம்.',
            faqSecurityQuestion: 'என் மருத்துவ தரவு பாதுகாப்பானதா?',
            faqSecurityAnswer: 'ஆம். நாங்கள் முழுமையாக <strong>HIPAA</strong> இணக்கமானவர்கள் மற்றும் அனைத்து பதிவேற்றப்பட்ட படங்கள் மற்றும் நோயாளி தரவுக்கு முழு-முதல்-முழு குறியாக்கத்தைப் பயன்படுத்துகிறோம். உங்கள் வெளிப்படையான அனுமதியின்றி உங்கள் படங்களை நிரந்தரமாக சேமிக்க மாட்டோம், உங்கள் தனியுரிமை எப்போதும் பாதுகாக்கப்படுவதை உறுதி செய்கிறோம்.',
            faqApiQuestion: 'இந்த API-ஐ என் கிளினிக் மென்பொருளில் ஒருங்கிணைக்க முடியுமா?',
            faqApiAnswer: 'நிச்சயமாக. நிலையான மின்னணு சுகாதார பதிவு (EHR) அமைப்புகளுடன் தடையின்றி ஒருங்கிணைக்க வடிவமைக்கப்பட்ட வலுவான RESTful API-ஐ வழங்குகிறோம். ஆவணங்கள் மற்றும் API விசைகளை கோர மேலே உள்ள தொடர்பு படிவத்தில் "கூட்டாண்மை வாய்ப்பு" என்பதை தேர்ந்தெடுக்கவும்.',
            faqTimeQuestion: 'பகுப்பாய்வுக்கு எவ்வளவு நேரம் ஆகும்?',
            faqTimeAnswer: 'பகுப்பாய்வு கிட்டத்தட்ட உடனடியானது. எங்கள் மேம்படுத்தப்பட்ட inference இயந்திரம் பொதுவாக உயர் தெளிவுத்திறன் படங்களை <strong>2 வினாடிகளுக்கும் குறைவாக</strong> செயலாக்குகிறது, உடனடி கருத்து மற்றும் பதிவிறக்கக்கூடிய PDF அறிக்கைகளை வழங்குகிறது.',
            faqConditionsQuestion: 'AI என்ன நிலைமைகளைக் கண்டறிய முடியும்?',
            faqConditionsAnswer: 'தற்போது, எங்கள் மாதிரிகள் <strong>ஈறு அழற்சி, சொத்தை (பற்சிதைவுகள்), மற்றும் பீரியோடோன்டிடிஸ்</strong>-ன் ஆரம்ப அறிகுறிகளைக் கண்டறிய பயிற்சி பெற்றுள்ளன. வாய் புற்றுநோய் திரையிடல் மற்றும் பல் சீரமைப்பு மதிப்பீடுகளை உள்ளடக்கியதாக எங்கள் தரவுத்தொகுப்பை தீவிரமாக விரிவாக்கி வருகிறோம்.',
            
            // Triage Page Additional
            intelligentOralAnalysis: 'புத்திசாலி வாய் நோய் பகுப்பாய்வு',
            triageSubtitle: 'மருத்துவ படங்கள் மற்றும் ஹிஸ்டோபத்தாலஜி ஸ்லைடுகளை துல்லியமாக வகைப்படுத்த அதிநவீன AI-ஐ பயன்படுத்துங்கள். தானியங்கி டிரியேஜ் செயல்முறையைத் தொடங்க உங்கள் மாதிரியைப் பதிவேற்றவும்.',
            supportsImageFormats: 'JPG, JPEG, PNG ஆதரிக்கப்படுகிறது (மருத்துவ அல்லது ஹிஸ்டோபத்தாலஜி)',
            securePrivateUpload: 'பாதுகாப்பான மற்றும் தனிப்பட்ட பதிவேற்றம்',
            analyzingImageStructure: 'பட அமைப்பை பகுப்பாய்வு செய்கிறது...',
            smartTriageFeatureDesc: 'காட்சி அம்சங்களின் அடிப்படையில் பதிவேற்றப்பட்ட படங்களை ஹிஸ்டோபத்தாலஜி அல்லது மருத்துவ திரையிடல் மாதிரிக்கு தானாக திசைதிருப்புகிறது.',
            histopathologyFeatureDesc: 'நுண்ணோக்கி ஸ்லைடுகளில் கட்டி கண்டறிதல், தரப்படுத்தல் மற்றும் ஊடுருவல் ஆழ அளவீடுக்கான ஆழ் கற்றல் பகுப்பாய்வு.',
            clinicalScreeningFeatureDesc: 'வாய் சுகாதார மதிப்பீடு மற்றும் சாத்தியமான புண்கள் அல்லது அசாதாரணங்களை அடையாளம் காண நிகழ்நேர பொருள் கண்டறிதல்.',
            
            // Model A Additional
            toggleFullscreen: 'முழுத்திரையை மாற்று',
            heatmapInfoNote: 'வெப்ப வரைபடங்கள் அதிக நிகழ்தகவு கட்டி பகுதிகளை காட்சிப்படுத்துகின்றன. ஒப்பிடுவதற்கு காட்சிகளுக்கு இடையே மாற்றவும்.',
            patternOfInvasion: 'ஊடுருவல் மாதிரி',
            perineuralInvasion: 'நரம்பு சுற்றி ஊடுருவல்',
            mitoticIndex: 'மைட்டோடிக் குறியீடு',
            tumourBudsCount: 'கட்டி மொட்டுக்கள் எண்ணிக்கை',
            viewAiRecommendation: 'AI பரிந்துரையைப் பார்க்கவும்',
            pdfReport: 'PDF அறிக்கை',
            emailReport: 'மின்னஞ்சல் அறிக்கை',
            startNewAnalysis: 'புதிய பகுப்பாய்வைத் தொடங்கு',
            
            // Model B Additional
            lowQualityImage: 'குறைந்த தரமான படம்',
            detections: 'கண்டறிதல்கள்',
            fullscreen: 'முழுத்திரை',
            screeningResult: 'திரையிடல் முடிவு',
            hygieneScore: 'சுகாதார மதிப்பெண்',
            waitingForAnalysis: 'பகுப்பாய்விற்காக காத்திருக்கிறது...',
            
            // Chat Widget Additional
            oralAiAssistant: 'Oral AI உதவியாளர்',
            onlineReady: 'ஆன்லைன் மற்றும் தயார்',
            minimize: 'சிறிதாக்கு',
            chatWelcomeMessage: 'வணக்கம்! நான் உங்கள் AI மருத்துவ உதவியாளர். உங்கள் பகுப்பாய்வு முடிவுகளை விளக்கவும் வாய் சுகாதாரம் பற்றிய பொது கேள்விகளுக்கு பதிலளிக்கவும் என்னால் உதவ முடியும்.',
            justNow: 'இப்போது',
            suggestedTopics: 'பரிந்துரைக்கப்பட்ட தலைப்புகள்',
            whatIsOralCancer: 'வாய் புற்றுநோய் என்றால் என்ன?',
            explainHistopathology: 'ஹிஸ்டோபத்தாலஜியை விளக்கவும்',
            howDoesAiWork: 'AI எவ்வாறு வேலை செய்கிறது?',
            chatInputPlaceholder: 'உங்கள் கேள்வியை உள்ளிடவும்...',
            aiDisclaimer: 'AI தவறுகள் செய்யலாம். முக்கியமான தகவலை சரிபார்க்கவும்.',
            
            // Department Page
            ourExperts: 'எங்கள் நிபுணர்கள்',
            meetTheTeam: 'அணியை சந்தியுங்கள்',
            departmentHeroDesc: 'Oral AI-க்கு பின்னால் உள்ள அற்புதமான மனங்கள், கூட்டுறவு மற்றும் புதுமை மூலம் பல் நோயறிதலை புரட்சிகரமாக்க அர்ப்பணிக்கப்பட்டவர்கள்.',
            systems: 'அமைப்புகள்',
            backendDesign: 'பின்னணி வடிவமைப்பு',
            backendDeveloper: 'பின்னணி உருவாக்குநர்',
            backendDevDesc: 'வலுவான API-களை உருவாக்கி உயர் செயல்திறன் மாதிரி inference இயந்திரங்களை நிர்வகித்தல்.',
            uiux: 'UI/UX',
            frontendDesign: 'முன்னணி வடிவமைப்பு',
            frontendDeveloper: 'முன்னணி உருவாக்குநர்',
            frontendDevDesc: 'தடையற்ற மருத்துவ பகுப்பாய்விற்கு உள்ளுணர்வு மற்றும் பதிலளிக்கக்கூடிய பயனர் இடைமுகங்களை உருவாக்குதல்.',
            dataTeam: 'தரவு அணி',
            datasetAnnotation: 'தரவுத்தொகுப்பு குறிப்பு & தயாரிப்பு',
            datasetAnnotationDesc: 'எங்கள் AI மாதிரிகளை பயிற்றுவிக்க உயர் தரமான தரவை உறுதி செய்தல்.',
            datasetSpecialist: 'தரவுத்தொகுப்பு நிபுணர்',
            datasetSpecialistDesc1: 'மருத்துவ படக் குறிப்பு மற்றும் தரவு முன்செயலாக்க பைப்லைன்களில் நிபுணர்.',
            datasetSpecialistDesc2: 'தரவு தரம் உத்தரவாதம் மற்றும் தரவுத்தொகுப்பு சமநிலை நுட்பங்களில் நிபுணத்துவம்.',
            datasetSpecialistDesc3: 'நோயியல் அம்ச பிரித்தெடுப்பு மற்றும் மெட்டாடேட்டா நிர்வாகத்தில் கவனம் செலுத்துகிறது.',
            
            // Blog Page
            oralAiJournal: 'Oral AI பத்திரிகை',
            blogHeroTitle: 'நுண்ணறிவுகள், புதுப்பிப்புகள் & கதைகள்',
            blogHeroDesc: 'எங்கள் தொழில்நுட்பம், நோயாளி சுகாதார வழிகாட்டிகள் மற்றும் பல் மருத்துவத்தில் AI-ன் எதிர்காலத்தில் ஆழமான பார்வைகள்.',
            engineering: 'பொறியியல்',
            featuredPostTitle: 'துல்லியத்தின் கட்டமைப்பு: Oral AI-ன் இரட்டை-மாதிரி அமைப்பின் உள்ளே',
            featuredPostDesc: '99.8% நோயறிதல் துல்லியத்தை அடைய நிபுணத்துவ மருத்துவ மற்றும் ஹிஸ்டோபத்தாலஜி மாதிரிகளுடன் ட்ரையேஜ் ரூட்டரை எவ்வாறு இணைத்தோம்.',
            readArticle: 'கட்டுரையைப் படிக்கவும்',
            ourBlog: 'எங்கள் வலைப்பதிவு',
            latestArticles: 'சமீபத்திய கட்டுரைகள்',
            patientHealth: 'நோயாளி சுகாதாரம்',
            blogPost1Title: 'புறக்கணிக்கக் கூடாத வாய் சுகாதார பிரச்சினைகளின் 5 ஆரம்ப அறிகுறிகள்',
            blogPost1Desc: 'நுட்பமான நிறமாற்றம் முதல் லேசான உணர்திறன் வரை, பிரச்சினை பெரிதாகும் முன் உங்கள் வாய் உங்களுக்கு என்ன சொல்ல முயற்சிக்கிறது என்பதை அறியுங்கள்.',
            behindTheScenes: 'திரைக்குப் பின்னால்',
            blogPost2Title: 'தரவிலிருந்து நோயறிதல் வரை: எங்கள் தரவுத்தொகுப்பை எவ்வாறு உருவாக்கினோம்',
            blogPost2Desc: 'எங்கள் AI உயர் தரமான மருத்துவ படங்களிலிருந்து கற்றுக்கொள்வதை உறுதி செய்ய எங்கள் தரவுத்தொகுப்பு அணி பயன்படுத்தும் கடுமையான செயல்முறையைப் பாருங்கள்.',
            futureTech: 'எதிர்கால தொழில்நுட்பம்',
            blogPost3Title: 'தொலை-பல் மருத்துவத்தின் எதிர்காலம்: முதல் பதிலளிப்பவராக AI',
            blogPost3Desc: 'உங்கள் ஸ்மார்ட்ஃபோனிலிருந்து ஆரம்ப நோயறிதலைப் பெறுவதை கற்பனை செய்யுங்கள். Oral AI தொலைநிலை திரையிடலை எவ்வாறு நிஜமாக்குகிறது என்பதை இங்கே காணலாம்.',
            
            // News/Pages Page
            industryInsights: 'தொழில் நுண்ணறிவுகள்',
            eraOfMedicalAi: 'மருத்துவ AI-ன் சகாப்தம்',
            pagesHeroDesc: 'செயற்கை நுண்ணறிவு எவ்வாறு சுகாதார நிலப்பரப்பை மறுவடிவமைக்கிறது என்பதை கண்டறியுங்கள், ஆரம்ப நோயறிதல் முதல் தனிப்பயனாக்கப்பட்ட சிகிச்சை திட்டங்கள் வரை.',
            diagnostics: 'நோயறிதல்',
            newsArticle1Title: 'ஆரம்ப புற்றுநோய் கண்டறிதலில் AI மனித நிபுணர்களை விஞ்சுகிறது',
            newsArticle1Desc: 'சமீபத்திய ஆய்வுகள் ஆழ் கற்றல் மாதிரிகள் மருத்துவ இமேஜிங்கில் ஆரம்ப நிலை அசாதாரணங்களை அடையாளம் காண 99% துல்லியத்தை அடைகின்றன, தவறான எதிர்மறைகளை கணிசமாக குறைக்கின்றன.',
            readFullStory: 'முழு கதையைப் படிக்கவும்',
            robotics: 'ரோபோடிக்ஸ்',
            newsArticle2Title: 'துல்லிய அறுவை சிகிச்சை: AI-உதவி செயல்பாடுகளின் எழுச்சி',
            newsArticle2Desc: 'அறுவை சிகிச்சை நிபுணர்கள் இப்போது AI-இயங்கும் ரோபோ கைகளை சப்-மில்லிமீட்டர் துல்லியத்துடன் சிக்கலான நடைமுறைகளை செய்ய பயன்படுத்துகின்றனர், நோயாளிகளின் மீட்பு நேரத்தை குறைக்கின்றனர்.',
            pharma: 'மருந்து',
            newsArticle3Title: 'மருந்து கண்டுபிடிப்பை விரைவுபடுத்துதல்',
            newsArticle3Desc: 'ஜெனரேட்டிவ் AI மூலக்கூறு தொடர்புகளை கணிப்பதன் மூலம் மருந்து மேம்பாட்டு காலவரிசைகளை ஆண்டுகளிலிருந்து மாதங்களாக குறைக்கிறது.',
            genomics: 'ஜீனோமிக்ஸ்',
            newsArticle4Title: 'ஹைப்பர்-தனிப்பயனாக்கப்பட்ட மருத்துவம்',
            newsArticle4Desc: 'ஜீனோமிக் தரவை பகுப்பாய்வு செய்யும் AI அல்காரிதங்கள் இப்போது ஒரு நபரின் DNA சுயவிவரத்திற்கு குறிப்பாக சிகிச்சை திட்டங்களை வடிவமைக்க முடியும்.',
            patientCare: 'நோயாளி பராமரிப்பு',
            newsArticle5Title: '24/7 மெய்நிகர் சுகாதார உதவியாளர்கள்',
            newsArticle5Desc: 'LLM-இயங்கும் சாட்போட்கள் உலகளவில் உடனடி, துல்லியமான மருத்துவ டிரையேஜ் மற்றும் மன நல ஆதரவை வழங்குகின்றன.',
            joinTheRevolution: 'புரட்சியில் சேருங்கள்',
            joinRevolutionDesc: 'இந்த மாற்றத்தின் முன்னணியில் Oral AI உள்ளது. இன்றே எங்கள் அதிநவீன நோயறிதல் கருவிகளை அனுபவியுங்கள்.',
            tryOralAiNow: 'இப்போது Oral AI-ஐ முயற்சிக்கவும்',
            
            // CTA Section
            trustedHealthcare: 'நம்பகமான சுகாதாரம்',
            empoweringEarlyDetection: 'ஆரம்ப கண்டறிதலை வலுப்படுத்துதல்<br>உயிர்களைக் காப்பாற்றுதல்.',
            joinThousandsDesc: 'விரைவான, துல்லியமான மற்றும் அணுகக்கூடிய வாய் சுகாதார திரையிடலுக்கு Oral AI-ஐ நம்பும் ஆயிரக்கணக்கான நோயாளிகள் மற்றும் மருத்துவர்களுடன் சேருங்கள்.',
            accuracyRate: 'துல்லிய விகிதம்',
            patientsScreened: 'திரையிடப்பட்ட நோயாளிகள்',
            aiAvailability: 'AI கிடைக்கும் தன்மை',
            supportLabel: 'ஆதரவு',
            needExpertAdvice: 'நிபுணர் ஆலோசனை தேவையா?',
            medicalTeamHelp: 'உங்கள் முடிவுகளை விளக்கவும் அடுத்த படிகளை வழிநடத்தவும் எங்கள் மருத்துவக் குழு உதவ தயாராக உள்ளது.',
            callUsNow: 'இப்போது அழைக்கவும்',
            emailSupport: 'மின்னஞ்சல் ஆதரவு',
            
            // Testimonials
            testimonialsLabel: 'சான்றுகள்',
            whatPatientsSay: 'எங்கள் நோயாளிகள் என்ன சொல்கிறார்கள்',
            testimonialsDesc: 'ஆரம்ப கண்டறிதல் மற்றும் மன அமைதிக்காக எங்கள் AI திரையிடல் கருவியைப் பயன்படுத்தியவர்களின் உண்மையான கதைகள்.',
            testimonial1: '"AI திரையிடல் நம்பமுடியாத அளவு வேகமாக இருந்தது. என் ஈறில் ஒரு புள்ளி பற்றி கவலைப்பட்டேன், கருவி உடனடி மதிப்பீடு கொடுத்து மருத்துவரைப் பார்க்க முடிவெடுக்க உதவியது."',
            testimonial2: '"புகைப்பிடிப்பவராக, வாய் சுகாதாரத்தைப் பற்றி கவலைப்படுகிறேன். இந்த செயலி மாற்றங்களைக் கண்காணிக்க உதவுகிறது. அறிக்கை உருவாக்கம் மிகவும் தொழில்முறை மற்றும் புரிந்துகொள்ள எளிதானது."',
            testimonial3: '"வருகைகளுக்கு இடையே சுய-கண்காணிப்புக்கு என் நோயாளிகளுக்கு இதை பரிந்துரைக்கிறேன். புண் கண்டறிதலின் துல்லியம் ஈர்க்கும் மற்றும் நம்பகமானது."',
            testimonial4: '"இடைமுகம் பயன்படுத்த மிகவும் எளிதானது. நான் ஒரு புகைப்படத்தை பதிவேற்றினேன், சில நொடிகளில் முடிவுகள் கிடைத்தன. என்னிடம் மிகவும் தேவைப்பட்டபோது மன அமைதி கொடுத்தது."',
            testimonial5: '"கல்வி நோக்கங்களுக்கும் சிறந்த கருவி. வெவ்வேறு வாய் நிலைகள் எப்படி இருக்கும் என்பதை காட்சிப்படுத்த உதவுகிறது. மாணவர்களுக்கு மிகவும் உதவிகரமானது."',
            testimonial6: '"குணமாகாத புண் பற்றி கவலைப்பட்டேன். செயலி நிபுணரைப் பார்க்க பரிந்துரைத்தது, அவ்வாறு செய்ததில் மகிழ்ச்சி. ஆரம்ப கண்டறிதல் வேலை செய்கிறது."',
            rolePatient: 'நோயாளி',
            roleRegularUser: 'வழக்கமான பயனர்',
            roleDentalHygienist: 'பல் சுகாதார நிபுணர்',
            roleStudent: 'மாணவர்',
            roleDoctor: 'மருத்துவர்',
            roleAdmin: 'நிர்வாகி',
            
            // Notifications
            notificationsTitle: 'அறிவிப்புகள்',
            markAllRead: 'அனைத்தையும் படித்ததாக குறிக்கவும்',
            noNewNotifications: 'புதிய அறிவிப்புகள் இல்லை',
            allCaughtUp: 'அனைத்தும் முடிந்தது!',
            noNewNotificationsOrAppointments: 'புதிய அறிவிப்புகள் அல்லது சந்திப்புகள் இல்லை.',
            
            // Model B Results
            qualityNoteLowRes: 'குறைந்த தெளிவுத்திறன். சிறந்த நிலைத்தன்மைக்கு நிலையான பயன்முறைக்கு மாற்றப்பட்டது.',
            screeningResultNormal: 'சாதாரணம்',
            screeningResultRefertoDentist: 'பல் மருத்துவரிடம் அனுப்பவும்',
            hygieneScoreHigh: 'உயர்',
            hygieneScoreMedium: 'நடுத்தரம்',
            hygieneScoreLow: 'குறைவு',
            noIssuesDetected: 'குறிப்பிட்ட சிக்கல்கள் கண்டறியப்படவில்லை.',
            detectedCount: '{count} கண்டறியப்பட்டது',
            conditionCaries: 'பல் சொத்தை',
            conditionGingivitis: 'ஈறு அழற்சி',
            conditionUlcer: 'புண்',
            conditionTooth: 'பல்',
            conditionCalculus: 'கால்குலஸ்',
            conditionHypodontia: 'ஹைபோடோன்டியா',
            
            // Model A Results
            tumourDetected: 'கட்டி கண்டறியப்பட்டது',
            noTumour: 'கட்டி இல்லை',
            detected: 'கண்டறியப்பட்டது',
            notDetected: 'கண்டறியப்படவில்லை',
            
            // Technology Modal
            techPytorchSubtitle: 'ஆழ் கற்றல் கட்டமைப்பு',
            techPytorchBeginner: "PyTorch, Facebook-ஆல் உருவாக்கப்பட்டது, நரம்பியல் வலையமைப்புகளை உருவாக்க பரவலாக பயன்படுத்தப்படும் மற்றொரு ஆழ் கற்றல் கட்டமைப்பாகும். அதன் நேரடியான, Pythonic தன்மை தொடக்கநிலையாளர்களுக்கு மாதிரி உருவாக்கம் மற்றும் பயிற்சியின் அடிப்படைகளை எளிதாக புரிந்துகொள்ள உதவுகிறது. தொடக்கநிலையாளர்கள் அதிக தொழில்நுட்ப மேல்நிலை பற்றி கவலைப்படாமல் படம் வகைப்படுத்தலுக்கான எளிய மாதிரிகளை உருவாக்குவதில் PyTorch-ன் நெகிழ்வுத்தன்மையை பாராட்டுவார்கள்.",
            techPytorchAdvanced: "மேம்பட்ட பயனர்கள் PyTorch-ன் டைனமிக் கம்ப்யூட்டேஷன் கிராஃப்பைப் பயன்படுத்தலாம், சிக்கலான கட்டிடக்கலைகள், தனிப்பயன் இழப்பு செயல்பாடுகள் மற்றும் ஆப்டிமைசர்களை உருவாக்கும்போது அதிக நெகிழ்வுத்தன்மையை அனுமதிக்கிறது. இது ஆராய்ச்சியாளர்களுக்கு சிறந்த தேர்வாகும், ஏனெனில் PyTorch விஷன் லேங்குவேஜ் மாடல்கள், ஜெனரேட்டிவ் அட்வர்சேரியல் நெட்வொர்க்ஸ் (GANs) மற்றும் ஆழ் ரீஇன்ஃபோர்ஸ்மென்ட் லேர்னிங் போன்ற அதிநவீன மாதிரிகளுடன் தடையற்ற சோதனையை வழங்குகிறது. அதன் திறமையான நினைவக மேலாண்மை மற்றும் GPU ஆதரவுக்கு நன்றி, பெரிய தரவுத்தொகுப்புகளை கையாள்வதிலும் சிறந்து விளங்குகிறது.",
            techCudaSubtitle: 'GPU முடுக்கம்',
            techCudaBeginner: "CUDA என்பது NVIDIA-ஆல் உருவாக்கப்பட்ட இணை கணினி தளம் மற்றும் நிரலாக்க மாதிரியாகும், அதே சமயம் cuDNN ஆழ் நரம்பியல் வலையமைப்புகளுக்கான GPU-முடுக்கப்பட்ட நூலகமாகும். தொடக்கநிலையாளர்களுக்கு, இந்த கருவிகள் தொழில்நுட்பமானவையாகத் தோன்றலாம், ஆனால் அவற்றின் முதன்மை நோக்கம் GPU சக்தியைப் பயன்படுத்தி ஆழ் கற்றல் மாதிரிகளின் பயிற்சியை விரைவுபடுத்துவதாகும். பயிற்சி சூழலில் CUDA மற்றும் cuDNN-ஐ சரியாக அமைப்பதன் மூலம், குறிப்பாக TensorFlow மற்றும் PyTorch போன்ற கட்டமைப்புகளுடன் வேலை செய்யும்போது, மாதிரி பயிற்சியின் வேகம் மற்றும் தேர்வுமுறையில் குறிப்பிடத்தக்க முன்னேற்றத்தை அடையலாம்.",
            techCudaAdvanced: "நிபுணர்கள் அதிக தேவை கொண்ட பயன்பாடுகளில் செயல்திறனை மேம்படுத்த CUDA மற்றும் cuDNN-ன் முழு சக்தியையும் பயன்படுத்தலாம். இது குறிப்பிட்ட செயல்பாடுகளுக்கான தனிப்பயன் CUDA கெர்னல்களை எழுதுதல், GPU நினைவகத்தை திறமையாக நிர்வகித்தல் மற்றும் அதிகபட்ச வேகம் மற்றும் அளவிடுதலுக்காக நரம்பியல் வலையமைப்பு பயிற்சியை நுணுக்கமாக சரிசெய்தல் ஆகியவை அடங்கும். பெரிய தரவுத்தொகுப்புகளுடன் வேலை செய்யும் மற்றும் தங்கள் மாதிரிகளிலிருந்து சிறந்த செயல்திறன் தேவைப்படும் டெவலப்பர்களுக்கு இந்த கருவிகள் அவசியமானவை.",
            techYoloSubtitle: 'நிகழ்நேர பொருள் கண்டறிதல்',
            techYoloBeginner: "YOLO (You Only Look Once) என்பது நிகழ்நேர பயன்பாடுகளுக்கு குறிப்பாக பிரபலமான வேகமான பொருள் கண்டறிதல் அல்காரிதமாகும். தொடக்கநிலையாளர்கள் ஒப்பீட்டளவில் எளிமையான குறியீட்டுடன் படங்கள் அல்லது வீடியோக்களில் பொருட்களை விரைவாக கண்டறிய முன்-பயிற்சி பெற்ற YOLO மாதிரிகளைப் பயன்படுத்தலாம். பயன்படுத்த எளிதானது என்பதால், சிக்கலான மாதிரிகளை புதிதாக உருவாக்காமல் பொருள் கண்டறிதலை ஆராய விரும்புவோருக்கு YOLO ஒரு சிறந்த நுழைவுப் புள்ளியாக அமைகிறது.",
            techYoloAdvanced: "YOLO குறிப்பிட்ட பொருட்களைக் கண்டறிய தனிப்பயன் தரவுத்தொகுப்புகளில் மாதிரிகளை நுணுக்கமாக சரிசெய்வதற்கான வாய்ப்புகளை வழங்குகிறது, கண்டறிதல் வேகம் மற்றும் துல்லியத்தை மேம்படுத்துகிறது. YOLO-வின் இலகு தன்மை மொபைல் சாதனங்கள் போன்ற வளம்-கட்டுப்படுத்தப்பட்ட சூழல்களில் பயன்படுத்த அனுமதிக்கிறது, நிகழ்நேர பயன்பாடுகளுக்கான சிறந்த தீர்வாக அமைகிறது. நிபுணர்கள் YOLO-வின் புதிய பதிப்புகளை பரிசோதிக்கலாம், குறிப்பிட்ட திட்ட தேவைகளுக்கு ஏற்ப அளவுருக்களை சரிசெய்யலாம்."
        }
    },
    
    // Initialize language system
    init() {
        const savedLang = localStorage.getItem('preferred_language') || 'en';
        this.current = savedLang;
        this.applyToPage();
    },
    
    // Get translation
    t(key) {
        const lang = this.translations[this.current] || this.translations.en;
        return lang[key] || key;
    },
    
    // Change language
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.current = lang;
            localStorage.setItem('preferred_language', lang);
            this.applyToPage();
            
            // Trigger custom event for other components to update
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
        }
    },
    
    // Apply translations to current page
    applyToPage() {
        document.documentElement.lang = this.current;
        
        // Update elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.placeholder) {
                    element.placeholder = translation;
                }
            } else {
                element.textContent = translation;
            }
        });
        
        // Update elements with data-translate-placeholder attribute
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            element.placeholder = this.t(key);
        });
        
        // Update elements with data-translate-title attribute
        document.querySelectorAll('[data-translate-title]').forEach(element => {
            const key = element.getAttribute('data-translate-title');
            element.title = this.t(key);
        });
        
        // Update elements with data-translate-aria attribute
        document.querySelectorAll('[data-translate-aria]').forEach(element => {
            const key = element.getAttribute('data-translate-aria');
            element.setAttribute('aria-label', this.t(key));
        });
        
        // Update navbar links
        this.updateNavbar();
        
        // Update footer links
        this.updateFooter();
        
        // Update language select if exists
        const langSelect = document.getElementById('languageSelect');
        if (langSelect) {
            langSelect.value = this.current;
        }
    },
    
    // Update navbar specifically
    updateNavbar() {
        const navLinks = {
            'nav-home': 'home',
            'nav-services': 'services'
        };
        
        Object.keys(navLinks).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                const key = navLinks[id];
                element.textContent = this.t(key);
            }
        });
        
        // Update nav-item-link elements
        document.querySelectorAll('.nav-item-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href === '/') link.textContent = this.t('home');
            else if (href === '/about') link.textContent = this.t('about');
            else if (href === '/department') link.textContent = this.t('department');
            else if (href === '/pages') link.textContent = this.t('news');
            else if (href === '/blog') link.textContent = this.t('blog');
            else if (href === '/contact') link.textContent = this.t('contact');
            else if (href.includes('showAnalysis')) link.textContent = this.t('services');
        });
    },
    
    // Update footer links
    updateFooter() {
        // Update footer links by class or specific selectors
        document.querySelectorAll('.footer-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href === '/') link.textContent = this.t('home');
            else if (href === '/about') link.textContent = this.t('aboutUs');
            else if (href === '/department') link.textContent = this.t('ourTeams');
            else if (href === '/privacy-policy') link.textContent = this.t('privacyPolicy');
            else if (href === '/terms-of-service') link.textContent = this.t('termsOfService');
            else if (href === '/cookie-policy') link.textContent = this.t('cookiePolicy');
            else if (href === '/hipaa-compliance') link.textContent = this.t('hipaaCompliance');
        });
    }
};

// Make it globally available and initialize immediately
if (typeof window !== 'undefined') {
    window.AppLanguage = AppLanguage;
    // Set current language immediately from localStorage (before DOMContentLoaded)
    const savedLang = localStorage.getItem('preferred_language');
    if (savedLang && AppLanguage.translations[savedLang]) {
        AppLanguage.current = savedLang;
    }
}

// Apply translations when DOM is ready
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        AppLanguage.init();
    });
}

# Android ProGuard rules
-keepattributes *Annotation*
-keepclassmembers class * {
    @<init>(<methods>);
}

-keep class **.R$* { *; }
-keep class * extends java.util.ListResourceBundle { *; }

# Gson library
-keep class com.google.gson.** { *; }
-keep class com.google.gson.examples.android.model.** { *; }

# Retrofit
-keep class retrofit2.** { *; }
-keep class retrofit2.http.* { *; }
-keep class okhttp3.** { *; }
-keep interface retrofit2.** { *; }

# AndroidX
-keep class androidx.** { *; }
-keep interface androidx.** { *; }

# Material Components
-keep class com.google.android.material.** { *; }
